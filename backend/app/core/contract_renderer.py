from decimal import ROUND_HALF_UP, Decimal
import subprocess
from typing import Dict, List
from docxtpl import DocxTemplate

from app.config import OUTPUT_DOCX_DIR, OUTPUT_PDF_DIR, TEMPLATE_PATH


class ContractRenderer:
    def __init__(self, data: List[str]) -> None:
        self.contract_number = f"YD{data[0]}"
        self.tpl = DocxTemplate(str(TEMPLATE_PATH))

        ton = float(data[2])
        price_per_ton = float(data[3])
        discount = float(data[4]) if data[4] else 0
        base_amount = ton * price_per_ton
        final_amount = base_amount - discount

        self.context: Dict[str, str] = {
            "contract_number": self.contract_number,
            "date": data[1],
            "ton": str(data[2]),
            "price": str(data[3]),
            "money": self.format_number(base_amount),
            "sub": self.format_number(discount) if discount != 0 else '',
            "all": self.format_number(final_amount),
            "upper": self.digital_to_chinese(self.format_number(final_amount)),

            "special": '优惠' if discount > 0 else '',

            "company_name": data[5],
            "tel": data[6],
            "address": self.ensure_line_break(data[7]),
            "identification_number": data[8],
            "opening_bank": data[9],
            "account": data[10],

            "pattern": data[11],

            "represent": data[12],
            "agent": data[13],
        }

    def format_number(self, money: int | float) -> str:
        """格式化金额为两位小数的字符串"""
        return f"{float(money):.2f}"

    def ensure_line_break(self, address: str) -> str:
        """地址不足一行时添加换行保持对齐"""
        return f"{address}\n" if len(address) <= 23 else address

    def digital_to_chinese(self, amount: str) -> str:
        """将数字金额转换为中文大写（人民币格式）"""
        # 定义中文数字和单位
        num_map = {"0": "零", "1": "壹", "2": "贰", "3": "叁",
                   "4": "肆", "5": "伍", "6": "陆", "7": "柒",
                   "8": "捌", "9": "玖"}
        unit_map = ["", "拾", "佰", "仟"]
        section_unit = ["", "万", "亿", "兆"]
        dec_unit = ["角", "分"]

        def four_digit_to_chinese(four_digits: str) -> str:
            result = []
            zero_flag = False
            for i in range(4):
                num = four_digits[i]
                unit = unit_map[3 - i]
                if num != "0":
                    if zero_flag:
                        result.append("零")
                        zero_flag = False
                    result.append(num_map[num] + unit)
                else:
                    zero_flag = True
            return "".join(result).rstrip("零")

        d = Decimal(str(amount)).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP)
        s = f"{d:.2f}"
        int_part, dec_part = s.split(".")

        # 整数部分处理
        if int_part == "0":
            int_result = "零元"
        else:
            int_result = ""
            int_part = int_part.zfill(((len(int_part) + 3) // 4) * 4)
            sections = [int_part[i:i+4] for i in range(0, len(int_part), 4)]
            result_parts = []
            zero_flag = False
            for idx, sec in enumerate(sections):
                part = four_digit_to_chinese(sec)
                if part:
                    if zero_flag:
                        result_parts.append("零")
                        zero_flag = False
                    result_parts.append(
                        part + section_unit[len(sections) - idx - 1])
                else:
                    zero_flag = True
            int_result = "".join(result_parts).lstrip("零") + "元"

        # 小数部分处理
        jiao, fen = dec_part[0], dec_part[1]
        if jiao == fen == "0":
            dec_result = "整"
        else:
            dec_result = ""
            if jiao != "0":
                dec_result += num_map[jiao] + dec_unit[0]
            if fen != "0":
                if jiao == "0":
                    dec_result += "零"
                dec_result += num_map[fen] + dec_unit[1]

        return int_result + dec_result

    def save_docx(self) -> str:
        """渲染并保存 .docx 文件"""
        filename = f"{self.contract_number}.docx"
        self.tpl.render(self.context)
        self.tpl.save(OUTPUT_DOCX_DIR / filename)
        return self.contract_number

    def convert_to_pdf(self, filename: str) -> None:
        """使用 LibreOffice 将 .docx 转换为 .pdf 并保存到 output/pdf 下"""
        docx_path = (OUTPUT_DOCX_DIR / f"{filename}.docx").resolve()
        try:
            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(OUTPUT_PDF_DIR),
                str(docx_path)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"LibreOffice 转换失败: {e}")
