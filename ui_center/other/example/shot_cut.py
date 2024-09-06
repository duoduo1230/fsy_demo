import sys
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QPixmap, QImage, QClipboard

app = QApplication(sys.argv)

# 创建一个 QWidget 作为容器
widget = QWidget()

# 创建一个 QVBoxLayout 布局
layout = QVBoxLayout(widget)

# 获取剪贴板中的图像
clipboard = app.clipboard()
image_data = clipboard.image(QClipboard.Clipboard)

if image_data:
    # 将图像转换为 QPixmap
    pixmap = QPixmap.fromImage(image_data)

    # 创建 QLabel 并设置图像
    label = QLabel()
    label.setPixmap(pixmap)

    # 将 QLabel 添加到布局中
    layout.addWidget(label)
else:
    print("剪贴板中没有图像数据。")

# 显示窗口
widget.show()

sys.exit(app.exec_())
