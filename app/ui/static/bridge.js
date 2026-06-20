// Minimal postMessage bridge to the platform host frame.
// Reads the iframe JWT from the URL hash the platform set (#jwt=..&page_id=..).
(function () {
  const params = new URLSearchParams(location.hash.slice(1));
  const jwt = params.get("jwt");
  const pageId = params.get("page_id");

  // Tell the host our height so it can size the iframe.
  function postResize() {
    parent.postMessage({ type: "resize", height: document.body.scrollHeight }, "*");
  }
  window.addEventListener("load", postResize);
  new ResizeObserver(postResize).observe(document.body);

  // Expose helpers for pages to call the platform / request a fresh token.
  window.addon = {
    jwt,
    pageId,
    toast: (level, message) => parent.postMessage({ type: "toast", level, message }, "*"),
    requestToken: () => parent.postMessage({ type: "request_token" }, "*"),
  };
})();
