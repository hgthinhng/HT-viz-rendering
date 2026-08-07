/**
 * kiemTraXml, SVG co phai XML hop le khong.
 *
 * Day la phep kiem quan trong nhat cua ca repo, va la phep suyt khong ai nghi ra.
 * Ca 12 chart ECharts tung KHONG hop le XML suot Phase 1 vi font stack boc bang
 * nhay kep bi nhung thang vao thuoc tinh `style="..."`, tao ra nhay kep long trong
 * nhay kep. Moi gate cu deu PASS vi chung chi DEM chuoi va DEM phan tu, khong cai
 * nao PARSE. Hau qua do duoc tren engine dich: WeasyPrint bo qua ca file, PDF ra
 * 0 net ve, chart bien mat sach ma khong bao loi. Trinh duyet van hien dung vi HTML
 * parser de tinh hon XML parser, nen soi bang mat tren ban HTML khong bao gio thay.
 *
 * Mot gate DEM duoc khong thay duoc mot gate PARSE.
 *
 * Dung python3 lam trong tai vi Node khong co san bo phan tich XML, va repo da phu
 * thuoc python3 san. Ve an toan: bo phan tich XML cua thu vien chuan dinh don XXE va
 * billion-laughs, nen o day dung THANG expat voi entity handler tu choi moi entity
 * thay vi goi ET.fromstring: expat khong tai external DTD, va handler duoi day cat
 * luon nhanh internal entity. Dau vao la SVG do chinh repo sinh ra nen be mat tan
 * cong bang 0; neu sau nay dung de nghiem thu SVG tu nguon NGOAI thi phai doi sang
 * defusedxml va them vao requirements.txt.
 */
import { execFileSync } from 'node:child_process';

const KIEM_XML_PY = `
import sys, xml.parsers.expat
p = xml.parsers.expat.ParserCreate()
def tu_choi_entity(*a, **k):
    raise xml.parsers.expat.ExpatError('tu choi entity, khong parse entity trong gate nay')
p.EntityDeclHandler = tu_choi_entity
p.ExternalEntityRefHandler = lambda *a: False
p.Parse(sys.stdin.buffer.read(), True)
`;

/**
 * @param {string} svg noi dung SVG
 * @returns {string} chuoi mo ta loi neu khong hop le, chuoi rong neu hop le
 */
export function kiemTraXml(svg) {
  try {
    execFileSync('python3', ['-c', KIEM_XML_PY], {
      input: svg,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return '';
  } catch (e) {
    const err = (e.stderr || '').toString().trim().split('\n').pop() || e.message;
    return err.replace(/^.*ParseError:\s*/, '');
  }
}
