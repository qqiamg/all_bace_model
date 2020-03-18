e = '0CoJUm6Qyw8W8jud';

for (var t = 16, n = [], r = 0; r < t; r++)
        n[r >>> 2] |= (255 & e.charCodeAt(r)) << 24  % 4 * 8;

console.info(n);
console.info(t);