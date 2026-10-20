import { loadPyodide } from '../vendor/pyodide/pyodide.mjs';

let runtimePromise;
self.onmessage = async ({ data }) => {
    try {
        runtimePromise ||= loadPyodide({ indexURL: new URL('../vendor/pyodide/', import.meta.url).href });
        const pyodide = await runtimePromise;
        // Disable network APIs after the pinned, same-origin runtime has loaded.
        self.fetch = () => Promise.reject(new Error('Network access is disabled in the course runner.'));
        self.XMLHttpRequest = undefined;
        self.WebSocket = undefined;
        self.postMessage({ ready: true });
        pyodide.runPython(`
import io, sys
class _PyBiteOutput(io.StringIO):
    limit = 20000
    truncated = False
    def write(self, text):
        remaining = self.limit - self.tell()
        if remaining <= 0:
            self.truncated = True
            return len(text)
        if len(text) > remaining:
            self.truncated = True
        return super().write(text[:remaining])
_py_bite_out = _PyBiteOutput()
_py_bite_err = _PyBiteOutput()
sys.stdout = _py_bite_out
sys.stderr = _py_bite_err
`);
        try {
            await pyodide.runPythonAsync(data.source);
            const stdout = pyodide.runPython("_py_bite_out.getvalue() + ('\\n… output truncated at 20,000 characters.' if _py_bite_out.truncated else '')");
            const stderr = pyodide.runPython("_py_bite_err.getvalue() + ('\\n… error output truncated at 20,000 characters.' if _py_bite_err.truncated else '')");
            self.postMessage({ stdout: stdout + (stderr ? `\n${stderr}` : '') });
        } catch (error) {
            const stderr = pyodide.runPython('_py_bite_err.getvalue()');
            self.postMessage({ error: `${error}\n${stderr}`.trim() });
        }
    } catch (error) {
        self.postMessage({ error: String(error) });
    }
};
