const hRange = [0, 360];
const sRange = [0, 100];
const lRange = [0, 100];

const getHashOfString = (str) => {
  const charArray = Array.from(str);
  return charArray.reduce((total, _char, index) => {
    return total += (str.charCodeAt(index) * index);
   }, 0);
}

const normalizeHash = (hash, min, max) => {
  return Math.floor((hash % (max - min)) + min);
};

function generateHSL(name) {
  const hash = getHashOfString(name);
  const h = normalizeHash(hash, hRange[0], hRange[1]);
  const s = normalizeHash(hash, sRange[0], sRange[1]);
  const l = normalizeHash(hash, lRange[0], lRange[1]);
  return [h, s, l];
}

const HSLtoString = (hsl) => {
  return `hsl(${hsl[0]}, ${hsl[1]}%, ${hsl[2]}%)`;
};

function createCanvas(primary, secondary) {
  var c = document.createElement("canvas");
  var ctx = c.getContext("2d");
  c.height = 150;
  c.width = 150;
  var my_gradient = ctx.createLinearGradient(0, 0, 150, 150);
  my_gradient.addColorStop(0, primary);
  my_gradient.addColorStop(1, secondary);
  ctx.fillStyle = my_gradient;
  ctx.fillRect(0, 0, 150, 150);
  return c;
}

function rgbToString(color) {
  var stringa = "rgb(" + color[0] + ", " + color[1] + ", " + color[2] + ")";
  return stringa;
}

function test() {
  primary = generateHSL("Sartori Leonardo");
  primaryRGB = hslToRgb(primary[0], primary[1], primary[2]);
  console.log(primaryRGB);
  secondaryRGB = [];
  for (const i in primaryRGB) {
    secondaryRGB.push(255 - primaryRGB[i]);
  }
  primaryRGBString = rgbToString(primaryRGB);
  secondaryRGBString = rgbToString(secondaryRGB);
  console.log(primaryRGBString, secondaryRGBString);
  var canvas = createCanvas(primaryRGBString, secondaryRGBString);
  //document.body.appendChild(convertCanvasToImage(canvas));
  return (convertCanvasToImageUrl(canvas));
}

function hslToRgb(h, s, l){
    s /= 100;
    l /= 100;
    const k = n => (n + h / 30) % 12;
    const a = s * Math.min(l, 1 - l);
    const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
    return [Math.round(255 * f(0)), Math.round(255 * f(8)), Math.round(255 * f(4))];
}

function convertCanvasToImage(canvas) {
  let image = new Image();
  //image.setAttribute("style", "width: 150px; height: 150px");
  image.src = canvas.toDataURL("image/png");
  return image;
}

function convertCanvasToImageUrl(canvas) {
  return canvas.toDataURL();
}

function convertStringToImageUrl(stringa) {
  primary = generateHSL(stringa);
  primaryRGB = hslToRgb(primary[0], primary[1], primary[2]);
  console.log(primaryRGB);
  secondaryRGB = [];
  for (const i in primaryRGB) {
    secondaryRGB.push(255 - primaryRGB[i]);
  }
  primaryRGBString = rgbToString(primaryRGB);
  secondaryRGBString = rgbToString(secondaryRGB);
  var canvas = createCanvas(primaryRGBString, secondaryRGBString);
  return convertCanvasToImageUrl(canvas);
}
