import { loadPyodide } from '../vendor/pyodide/pyodide.mjs';

let runtimePromise;
let inputLines = [];

function explainRuntimeError(error) {
    const message = String(error);
    if (/emscripten does not support processes/i.test(message)) {
        return 'This code tried to start an operating-system process. The browser Python runner cannot launch programs or run shell commands. Save the code as a .py file and run it in a local Python environment or isolated lab with the required tools installed. Use only systems you are authorized to test.';
    }
    return message;
}

self.onmessage = async ({ data }) => {
    try {
        const incomingLines = Array.isArray(data.stdinLines) ? data.stdinLines : [];
        if (incomingLines.length > 100) throw new Error('Program input is limited to 100 lines.');
        if (incomingLines.some(line => typeof line !== 'string')) throw new Error('Program input must contain text lines.');
        const inputSize = incomingLines.reduce((total, line) => total + line.length, 0);
        if (inputSize > 20000) throw new Error('Program input is limited to 20,000 characters.');
        inputLines = incomingLines.slice();
        runtimePromise ||= loadPyodide({
            indexURL: new URL('../vendor/pyodide/', import.meta.url).href,
            stdin: () => inputLines.length ? inputLines.shift() : null
        });
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
            const friendlyError = explainRuntimeError(error);
            const isProcessLimit = friendlyError !== String(error);
            self.postMessage({ error: isProcessLimit ? friendlyError : `${error}\n${stderr}`.trim() });
        }
    } catch (error) {
        self.postMessage({ error: String(error) });
    }
};
