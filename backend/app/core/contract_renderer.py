from decimal import ROUND_HALF_UP, Decimal
import subprocess
from typing import Dict, List
from docxtpl import DocxTemplate

from app.config import OUTPUT_DOCX_DIR, OUTPUT_PDF_DIR, TEMPLATE_PATH


class ContractRenderer:
    def __init__(self, data: List[str]) -> None:
        self.contract_number = f"YD{data[0]}"
        self.tpl = DocxTemplate(str(TEMPLATE_PATH))

        ton = float(data[3])
        price_per_ton = float(data[4])
        discount = float(data[5]) if data[5] else 0
        base_amount = ton * price_per_ton
        final_amount = base_amount - discount

        self.context: Dict[str, str] = {
            "contract_number": self.contract_number,
            "date": data[1],
            "company_name": data[2],

            "ton": str(data[3]),
            "price": str(data[4]),
            "money": self.format_number(base_amount),
            "sub": self.format_number(discount) if discount != 0 else '',
            "all": self.format_number(final_amount),
            "upper": self.digital_to_chinese(self.format_number(final_amount)),

            "special": '优惠' if discount > 0 else '',

            "tel": data[6],
            "address": self.ensure_line_break(data[7]),

            "represent": data[8],
            "agent": data[9],

            "identification_number": data[10],
            "opening_bank": data[11],
            "account": data[12],
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
        unit_int = ["元", "拾", "佰", "仟", "万", "拾", "佰", "仟",
                    "亿", "拾", "佰", "仟", "兆", "拾", "佰", "仟"]
        unit_dec = ["角", "分"]

        # 将输入转换为 Decimal 并保留两位小数
        d = Decimal(str(amount)).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP)
        s = f"{d:.2f}"
        int_part, dec_part = s.split(".")

        result = []

        # 处理整数部分
        int_len = len(int_part)
        for i, ch in enumerate(int_part):
            num = num_map[ch]
            unit = unit_int[int_len - i - 1]
            # 只在数字不为“0”时添加对应单位；遇到“0”时，若前一位不是“零”则添加“零”
            if ch != "0":
                result.append(num + unit)
            else:
                if result and result[-1] != "零":
                    result.append("零")

        # 去掉末尾多余的“零”
        if result and result[-1] == "零":
            result.pop()
        # 如果整个整数部分都是 0，补“零元”
        if not result:
            result.append("零元")
        else:
            # 如果最后一位不是“元”，补上“元”
            if not result[-1].endswith("元"):
                result.append("元")

        # 处理小数部分
        jiao, fen = dec_part[0], dec_part[1]
        if jiao == fen == "0":
            result.append("整")
        else:
            if jiao != "0":
                result.append(num_map[jiao] + unit_dec[0])
            else:
                # 如果“角”为0而“分”不为0，需要补“零”
                if fen != "0":
                    result.append("零")
            if fen != "0":
                result.append(num_map[fen] + unit_dec[1])

        return "".join(result)

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
