$(document).ready(function () {
  addPhotos();

  new fullpage('#fullpage', {
    autoScrolling: true,
    scrollHorizontally: true,
    scrollingSpeed: 1100, // Snappier but still cinematic transition
    easingcss3: 'cubic-bezier(0.23, 1, 0.32, 1)', // Apple-style easeOutQuint for snappiness
    fitToSection: true,
    fitToSectionDelay: 300,
    touchSensitivity: 15, // Reduced sensitivity for touch devices
    keyboardScrolling: true,
    animateAnchor: true,
    recordHistory: false,
    scrollBar: false,
    sectionSelector: '.section',
    lazyLoading: true,
    // Prevention of rapid skipping and cinematic pacing
    onLeave: function(origin, destination, direction) {
      // Slow down the transition start slightly
    },
    afterLoad: function(origin, destination, direction) {
      // Force a "pacing delay" - user must wait 600ms before scrolling again
      fullpage_api.setAllowScrolling(false);
      fullpage_api.setKeyboardScrolling(false);
      
      setTimeout(function() {
        fullpage_api.setAllowScrolling(true);
        fullpage_api.setKeyboardScrolling(true);
      }, 300); // Reduced "breath" for better responsiveness
    }
  });

  const giftLink = document.getElementById("giftLink");
  if (giftLink) {
    giftLink.addEventListener("click", function (e) {
      e.preventDefault();
      
      // Visual feedback
      giftLink.innerText = "SENDING...";
      giftLink.style.opacity = "0.7";
      giftLink.style.pointerEvents = "none";

      fetch(this.href)
        .then(response => {
          if (response.status === 204 || response.ok) {
            swal(
              'Sent Successfully!',
              'Check your email for your birthday surprise!',
              'success'
            );
          } else {
            throw new Error('Failed to send');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          swal(
            'Oops!',
            'Something went wrong. Please try again later.',
            'error'
          );
        })
        .finally(() => {
          giftLink.innerText = "GIFT";
          giftLink.style.opacity = "1";
          giftLink.style.pointerEvents = "auto";
        });
    });
  }

  // Soul Quotes Engine
  const soulQuotes = [
    "Leadership is the quiet art of making others better in your presence.",
    "A vision without boundaries, a heart without fear.",
    "Strength isn't just power; it's the patience to build something that lasts.",
    "In every challenge, she found a lesson; in every lesson, a new horizon.",
    "Ambition is the fuel, but kindness is the compass.",
    "The CTO of her own destiny, architecting a future of brilliance.",
    "Resilience is blooming even in the most unexpected places.",
    "Clarity of thought, presence of soul, and the courage to lead.",
    "Innovation starts with a dream and ends with the determination to build it.",
    "A presence that feels like poetry, a mind that thinks in light.",
    "Kindness is the ultimate form of sophistication.",
    "Building bridges between dreams and reality, one hackathon at a time.",
    "The most beautiful thing you can wear is your own confidence.",
    "A soul that carries responsibility with maturity and grace.",
    "Her story is just beginning, and every chapter is a masterpiece."
  ];

  let currentQuoteIndex = 0;
  const quoteElement = document.getElementById('dynamicQuote');

  if (quoteElement) {
    setInterval(() => {
      quoteElement.style.opacity = 0;
      quoteElement.style.transform = 'translateY(10px)';
      
      setTimeout(() => {
        currentQuoteIndex = (currentQuoteIndex + 1) % soulQuotes.length;
        quoteElement.textContent = `"${soulQuotes[currentQuoteIndex]}"`;
        quoteElement.style.opacity = 1;
        quoteElement.style.transform = 'translateY(0)';
      }, 800); // Wait for fade out
    }, 5000); // 5 second interval
  }
});

function select(selector) {
  var method = selector.substr(0, 1) == '.' ? 'getElementsByClassName' : 'getElementById';
  return document[method](selector.substr(1));
}

function range() {
  var range = { left: { x: [], y: [] }, right: { x: [], y: [] } };
  var wrap = {
    w: select("#wrap").clientWidth,
    h: select("#wrap").clientHeight
  }
  var photo = {
    w: select(".photo")[0].clientWidth,
    h: select(".photo")[0].clientHeight
  }
  range.wrap = wrap;
  range.photo = photo;

  range.left.x = [0, wrap.w / 2 - photo.w / 2];
  range.left.y = [0, wrap.h - photo.w / 2];
  range.right.x = [wrap.w / 2 + photo.w / 2, wrap.w];
  range.right.y = [0, wrap.h - photo.w / 2];

  return range;
}

function sort(n) {
  var _photo = select('.photo');
  var photos = Array.from(_photo);
  photos.forEach(p => {
    p.classList.remove('photo_center', 'photo_front', 'photo_back');
    p.classList.add('photo_front');
    p.style.left = '0';
    p.style.top = '0';
    p.style.margin = '0';
  });
  var photo_center = select('#photo_' + n);
  photo_center.classList.add('photo_center');

  var ranges = range();
  var center_left = ranges.wrap.w / 2 - ranges.photo.w / 2;
  var center_top = ranges.wrap.h / 2 - ranges.photo.h / 2;
  photo_center.style['transform'] = 'translate3d(' + center_left + 'px,' + center_top + 'px, 0) rotate(0deg) scale(1.4)';
  photo_center.style['-webkit-transform'] = 'translate3d(' + center_left + 'px,' + center_top + 'px, 0) rotate(0deg) scale(1.4)';
  photo_center.style['z-index'] = '999';

  photo_center = photos.splice(n, 1)[0];

  var photos_left = photos.splice(0, Math.ceil(photos.length / 2));
  var photos_right = photos;

  for (var i = 0; i < photos_left.length; i++) {
    var left = random(ranges.left.x);
    var top = random(ranges.left.y);
    var rotate = random([-150, 150]);
    photos_left[i].style['transform'] = 'translate3d(' + left + 'px,' + top + 'px, 0) rotate(' + rotate + 'deg) scale(1)';
    photos_left[i].style['-webkit-transform'] = 'translate3d(' + left + 'px,' + top + 'px, 0) rotate(' + rotate + 'deg) scale(1)';
  }
  for (var i = 0; i < photos_right.length; i++) {
    var left = random(ranges.right.x);
    var top = random(ranges.right.y);
    var rotate = random([-150, 150]);
    photos_right[i].style['transform'] = 'translate3d(' + left + 'px,' + top + 'px, 0) rotate(' + rotate + 'deg) scale(1)';
    photos_right[i].style['-webkit-transform'] = 'translate3d(' + left + 'px,' + top + 'px, 0) rotate(' + rotate + 'deg) scale(1)';
  }
  var navs = select('.i');
  Array.from(navs).forEach(nav => nav.classList.remove('i_current', 'i_back'));
  select('#nav_' + n).classList.add('i_current');
}

function random(range) {
  var max = Math.max(range[0], range[1]);
  var min = Math.min(range[0], range[1]);
  var diff = max - min;
  var number = Math.floor(Math.random() * diff + min);
  return number;
}

var data = data;
function addPhotos() {
  var template = select('#wrap').innerHTML;
  var html = [];
  var nav = [];
  for (i = 0; i < data.length; i++) {
    var _html = template.replace('{{index}}', i)
      .replace('{{img}}', data[i].img)
      .replace('{{caption}}', data[i].caption)
      .replace('{{desc}}', data[i].desc);
    html.push(_html);
    nav.push('<span id="nav_' + i + '" class="i" onclick ="turn(select(\'#photo_' + i + '\'))">&nbsp;</span>');
  }
  html.push('<div class="nav">' + nav.join('') + '</div>');
  select('#wrap').innerHTML = html.join('');
  sort(random([0, data.length]));
}


function turn(elem) {
  var cls = elem.className;
  var n = elem.id.split("_")[1];

  if (! /photo_center/.test(cls)) {
    return sort(n);
  }

  if (elem.classList.contains('photo_front')) {
    elem.classList.replace('photo_front', 'photo_back');
    select('#nav_' + n).classList.add('i_back');
  } else {
    elem.classList.replace('photo_back', 'photo_front');
    select('#nav_' + n).classList.remove('i_back');
  }
  return true;
}

// Robust Image Loader: Supports both .jpg and .jpeg
function handleImageError(img) {
    const src = img.src;
    if (src.includes('.jpg.jpeg')) {
        // Try fallback to just .jpg
        img.src = src.replace('.jpg.jpeg', '.jpg');
    } else if (src.endsWith('.jpg')) {
        // Try fallback to .jpeg or .jpg.jpeg
        img.src = src.replace('.jpg', '.jpeg');
        // If that also fails, it will trigger another error, so we should be careful
        img.onerror = function() {
            if (this.src.endsWith('.jpeg')) {
                this.src = this.src.replace('.jpeg', '.jpg.jpeg');
                this.onerror = null; // Stop infinite loop
            }
        };
    } else if (src.endsWith('.jpeg')) {
        img.src = src.replace('.jpeg', '.jpg');
        img.onerror = null;
    }
}



