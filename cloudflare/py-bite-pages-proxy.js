const PAGE_ORIGIN = 'py-bite.pages.dev';
const FORWARDED_HEADERS = [
  'accept',
  'accept-language',
  'cache-control',
  'if-modified-since',
  'if-none-match',
  'range',
];

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', {
        status: 405,
        headers: { Allow: 'GET, HEAD' },
      });
    }

    const source = new URL(request.url);
    const target = new URL(source.pathname + source.search, `https://${PAGE_ORIGIN}`);
    const headers = new Headers();
    for (const name of FORWARDED_HEADERS) {
      const value = request.headers.get(name);
      if (value) headers.set(name, value);
    }

    return fetch(target, {
      method: request.method,
      headers,
      redirect: 'follow',
    });
  },
};
