const pptxgen = require('pptxgenjs');
const path = require('path');
const html2pptx = require('./html2pptx.js');

(async () => {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5 inch, matches 960x540pt

  try {
    const { slide, placeholders } = await html2pptx('./slide-test-imgfix.html', pres);
    console.log('SUCCESS. placeholders:', JSON.stringify(placeholders, null, 2));
  } catch (e) {
    console.error('CONVERSION ERROR:');
    console.error(e.message);
    process.exitCode = 1;
    return;
  }

  await pres.writeFile({ fileName: 'output.pptx' });
  console.log('Wrote output.pptx');
})();
