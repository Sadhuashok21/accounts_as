// Delay GA4 by 3 seconds after the page load
window.addEventListener('load', function () {
  setTimeout(function () {
    var script = document.createElement('script');
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-WN9BKPTPEX';
    script.async = true;
    document.head.appendChild(script);

    // Initialize gtag only after script loads
    script.onload = function () {
      window.dataLayer = window.dataLayer || [];
      function gtag(){ dataLayer.push(arguments); }
      window.gtag = gtag;

      gtag('js', new Date());
      gtag('config', 'G-WN9BKPTPEX');
    };
  }, 3000); // delay in milliseconds
});
