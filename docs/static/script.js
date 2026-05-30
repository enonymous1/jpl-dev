/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  var sidenav = document.getElementById("mySidenav");
  if (sidenav.style.width === "250px") {
    closeNav();
  } else {
    sidenav.style.width = "250px";
    document.getElementById("content-wrapper").style.marginLeft = "250px";
  }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("content-wrapper").style.marginLeft = "0";
}

function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

function updateTooltipAlignment(icon) {
  const tooltipOffset = 260; // approximate tooltip width for edge detection
  const rect = icon.getBoundingClientRect();
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  icon.classList.remove('tooltip-left', 'tooltip-right', 'tooltip-bottom');

  if (rect.top < 100 && rect.bottom + 120 < viewportHeight) {
    icon.classList.add('tooltip-bottom');
    return;
  }

  if (rect.right + tooltipOffset > viewportWidth - 16) {
    icon.classList.add('tooltip-right');
    return;
  }

  if (rect.left < tooltipOffset) {
    icon.classList.add('tooltip-left');
    return;
  }
}

function updateAllTooltipAlignments() {
  document.querySelectorAll('.info-icon[data-tooltip]').forEach(icon => {
    updateTooltipAlignment(icon);
  });
}

function initializeSmartTooltips() {
  const icons = document.querySelectorAll('.info-icon[data-tooltip]');
  if (!icons.length) {
    return;
  }

  icons.forEach(icon => {
    if (!icon.hasAttribute('tabindex')) {
      icon.setAttribute('tabindex', '0');
    }

    icon.addEventListener('mouseenter', () => updateTooltipAlignment(icon));
    icon.addEventListener('focus', () => updateTooltipAlignment(icon));
    icon.addEventListener('blur', () => icon.classList.remove('tooltip-left', 'tooltip-right', 'tooltip-bottom'));
    icon.addEventListener('mouseleave', () => icon.classList.remove('tooltip-left', 'tooltip-right', 'tooltip-bottom'));
  });

  updateAllTooltipAlignments();
  window.addEventListener('resize', debounce(updateAllTooltipAlignments, 100));
}

document.addEventListener('DOMContentLoaded', initializeSmartTooltips);
