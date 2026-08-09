// registry.mjs, so ghi danh MOT nguon cho toan bo 23 preset ECharts.
//
// Import moi preset MOT LAN, gom lai theo TEN FILE (khong duoi .mjs) thanh { option,
// MAC_DINH }. An toan de import o ca hai lan: import chi keo option()/MAC_DINH ra, KHONG
// tu chay render nao (moi preset boc phan CLI trong `if (import.meta.url === ...)`, chi
// chay khi goi TRUC TIEP bang `node NN-ten.mjs`, khong chay khi bi import).
import * as p01 from './01-waterfall.mjs';
import * as p02 from './02-sankey.mjs';
import * as p03 from './03-bullet.mjs';
import * as p04 from './04-dumbbell.mjs';
import * as p05 from './05-slope.mjs';
import * as p06 from './06-tornado.mjs';
import * as p07 from './07-small-multiples.mjs';
import * as p08 from './08-heatmap.mjs';
import * as p09 from './09-candlestick.mjs';
import * as p10 from './10-treemap.mjs';
import * as p11 from './11-stacked-100.mjs';
import * as p12 from './12-area-stack.mjs';
import * as p13 from './13-line-annotated.mjs';
import * as p14 from './14-bar-ranking.mjs';
import * as p15 from './15-quadrant-scatter.mjs';
import * as p16 from './16-dot-distribution.mjs';
import * as p17 from './17-football-field.mjs';
import * as p18 from './18-sensitivity-grid.mjs';
import * as p19 from './19-raincloud.mjs';
import * as p20 from './20-ridgeline.mjs';
import * as p21 from './21-upset.mjs';
import * as p22 from './22-alluvial.mjs';
import * as p23 from './23-waffle.mjs';

export const PRESETS = {
  '01-waterfall': { option: p01.option, MAC_DINH: p01.MAC_DINH },
  '02-sankey': { option: p02.option, MAC_DINH: p02.MAC_DINH },
  '03-bullet': { option: p03.option, MAC_DINH: p03.MAC_DINH },
  '04-dumbbell': { option: p04.option, MAC_DINH: p04.MAC_DINH },
  '05-slope': { option: p05.option, MAC_DINH: p05.MAC_DINH },
  '06-tornado': { option: p06.option, MAC_DINH: p06.MAC_DINH },
  '07-small-multiples': { option: p07.option, MAC_DINH: p07.MAC_DINH },
  '08-heatmap': { option: p08.option, MAC_DINH: p08.MAC_DINH },
  '09-candlestick': { option: p09.option, MAC_DINH: p09.MAC_DINH },
  '10-treemap': { option: p10.option, MAC_DINH: p10.MAC_DINH },
  '11-stacked-100': { option: p11.option, MAC_DINH: p11.MAC_DINH },
  '12-area-stack': { option: p12.option, MAC_DINH: p12.MAC_DINH },
  '13-line-annotated': { option: p13.option, MAC_DINH: p13.MAC_DINH },
  '14-bar-ranking': { option: p14.option, MAC_DINH: p14.MAC_DINH },
  '15-quadrant-scatter': { option: p15.option, MAC_DINH: p15.MAC_DINH },
  '16-dot-distribution': { option: p16.option, MAC_DINH: p16.MAC_DINH },
  '17-football-field': { option: p17.option, MAC_DINH: p17.MAC_DINH },
  '18-sensitivity-grid': { option: p18.option, MAC_DINH: p18.MAC_DINH },
  '19-raincloud': { option: p19.option, MAC_DINH: p19.MAC_DINH },
  '20-ridgeline': { option: p20.option, MAC_DINH: p20.MAC_DINH },
  '21-upset': { option: p21.option, MAC_DINH: p21.MAC_DINH },
  '22-alluvial': { option: p22.option, MAC_DINH: p22.MAC_DINH },
  '23-waffle': { option: p23.option, MAC_DINH: p23.MAC_DINH },
};
