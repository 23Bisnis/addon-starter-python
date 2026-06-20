// Minimal postMessage bridge to the platform host frame.
// The platform delivers the iframe context JWT either in the URL hash (#jwt=..&page_id=..)
// or as a query param (?jwt=..). The server-side page route reads ?jwt=; we read both here
// so client-side code can also access the token.
(function () {
  const hashParams = new URLSearchParams(location.hash.slice(1));
  const queryParams = new URLSearchParams(location.search);
  const jwt = hashParams.get("jwt") || queryParams.get("jwt");
  const pageId = hashParams.get("page_id") || queryParams.get("page_id");

  // TODO: replace "*" with the platform's known origin (your manifest's postmessage_origin,
  // e.g. "https://app.23bisnis.com") to prevent leaking these messages to other embeds.
  const PLATFORM_ORIGIN = "*";

  // Tell the host our height so it can size the iframe.
  function postResize() {
    parent.postMessage({ type: "resize", height: document.body.scrollHeight }, PLATFORM_ORIGIN);
  }
  window.addEventListener("load", postResize);
  new ResizeObserver(postResize).observe(document.body);

  // Expose helpers for pages to call the platform / request a fresh token.
  window.addon = {
    jwt,
    pageId,
    toast: (level, message) => parent.postMessage({ type: "toast", level, message }, PLATFORM_ORIGIN),
    requestToken: () => parent.postMessage({ type: "request_token" }, PLATFORM_ORIGIN),
  };
})();
