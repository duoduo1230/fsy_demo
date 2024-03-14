#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict

from dayu_widgets import static
from ui_center.resource_widget.wizards.MSeparator import MHSeparator
from Qt.QtWidgets import *
from Qt.QtCore import *

# import net_log


default_qss_file = os.path.join(os.path.dirname(__file__), "main.qss")
with open(default_qss_file, 'r') as f:
    default_qss = f.read()


def dayu_css(css_content=None):
    def wrapper1(func):
        def new_init(*args, **kwargs):
            result = func(*args, **kwargs)
            instance = args[0]
            instance.setStyleSheet(css_content if css_content else default_qss)
            return result

        return new_init

    return wrapper1


class MWizardField(object):
    def __init__(self, page, name, getter, setter=None, signal=None, required=False):
        self.name = name
        self.setter = setter
        self.getter = getter
        self.signal = signal
        self.required = required
        self.page = page
        if required and (signal is None):
            raise Exception('You must give a signal when required is True')


class FieldMixin(object):
    field_dict = defaultdict(None)

    def register_field(self, name, getter, setter=None, signal=None, required=False):
        if name in self.fields():
            raise Exception('Field name {} already exists'.format(name))
        f = MWizardField(self, name, getter, setter, signal, required)
        self.field_dict.update({name: f})
        return f

    def fields(self):
        return self.field_dict.keys()

    def field(self, name):
        getter = self.field_dict[name].getter
        if callable(getter):
            return getter()
        else:
            return getter

    def set_field(self, name, arg):
        setter = self.field_dict[name].setter
        if callable(setter):
            setter(arg)
        else:
            self.field_dict[name].getter = arg


class MWizardPage(QWidget, FieldMixin):
    sig_complete_changed = Signal()

    def __init__(self, subtitle=None, parent=None):
        super(MWizardPage, self).__init__(parent)
        self.field_dict = defaultdict(None)
        self.wizard = parent
        self.initialized = False
        self.subtitle = subtitle

    def init_page(self):
        pass

    def is_complete(self):
        for name, f_obj in self.field_dict.items():
            if f_obj.required:
                if not self.field(name):
                    return False
        return True

    def callback(self, *args, **kwargs):
        pass


class MStepLabel(QLabel):
    def __init__(self, index, parent=None):
        super(MStepLabel, self).__init__(parent)
        self.setObjectName('wizard-step')
        self.setAlignment(Qt.AlignCenter)
        self.status = 'waiting'
        self.index = index

    def set_title(self, text):
        self.setText(
            '<span style="font-size:13pt;font-weight:bold;">Step {}</span><br/>{}'.format(self.index + 1, text))

    def set_status(self, status):
        self.status = status


class MWizard(QDialog, FieldMixin):

    sig_next_step = Signal(int)

    @dayu_css()
    def __init__(self, parent=None):
        super(MWizard, self).__init__(parent)

        self.field_dict = defaultdict(None)
        self.step_label_list = []

        self.title_label = QLabel()
        self.title_label.setObjectName('wizard-title')
        self.title_label.setAlignment(Qt.AlignCenter)
        step_frame = QFrame()
        step_frame.setObjectName('wizard-frame')
        self.step_lay = QHBoxLayout()
        self.step_lay.setContentsMargins(0, 0, 0, 0)
        self.step_lay.setSpacing(0)
        step_frame.setLayout(self.step_lay)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName('wizard-subtitle')
        self.stacked_lay = QStackedLayout()

        self.next_button = QPushButton('Next')
        self.previous_button = QPushButton('Previous')
        self.previous_button.setVisible(False)

        self.previous_button.clicked.connect(self.slot_back)
        self.next_button.clicked.connect(self.slot_next)

        button_lay = QHBoxLayout()
        button_lay.addStretch()
        button_lay.addWidget(self.previous_button)
        button_lay.addWidget(self.next_button)
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)
        main_lay.addWidget(self.title_label)
        main_lay.addWidget(step_frame)
        main_lay.addSpacing(20)
        main_lay.addWidget(self.subtitle_label)
        main_lay.addWidget(MHSeparator())
        main_lay.addLayout(self.stacked_lay)
        main_lay.addWidget(MHSeparator())
        main_lay.addLayout(button_lay)

    def add_page(self, page):
        index = self.stacked_lay.addWidget(page)
        page.wizard = self
        page.sig_complete_changed.connect(self._update_button_states)
        for f in page.field_dict.values():
            self.combine_field(f)

        label = MStepLabel(index)
        label.set_title(page.subtitle)
        self.subtitle_label.setText(page.subtitle)
        self.step_lay.addWidget(label)
        self.step_label_list.append(label)

        return index

    def combine_field(self, field):
        if field.name in self.fields():
            raise Exception('Field name {} already exists'.format(field.name))
        self.field_dict.update({field.name: field})
        if field.required and field.signal:
            field.signal.connect(field.page.sig_complete_changed)

    def current_id(self):
        return self.stacked_lay.currentIndex()

    def current_page(self):
        return self.stacked_lay.currentWidget()

    def set_title(self, text):
        self.title_label.setText(text)
        self.setWindowTitle(text)

    def _update_button(self, index):
        self.previous_button.setVisible(False if index == 0 else True)
        self.next_button.setText('Finish' if index == (self.stacked_lay.count() - 1) else 'Next')

    def _update_step(self, index):
        for i, label in enumerate(self.step_label_list):
            if i == index:
                label.setProperty('status', 'current')
                label.setEnabled(True)
            elif i < index:
                label.setProperty('status', 'passed')
                label.setEnabled(True)
            else:
                label.setProperty('status', 'waiting')
                label.setEnabled(False)
            self.style().polish(label)

    @Slot()
    def slot_back(self):
        current_id = self.stacked_lay.currentIndex()
        self.go_to(current_id - 1)

    @Slot()
    def slot_next(self):
        index = self.next_id()
        if index == -1:
            self.accept()
        self.go_to(index)
        self.sig_next_step.emit(index)

    def go_to(self, index):
        self.stacked_lay.setCurrentIndex(index)
        page = self.current_page()
        if not page.initialized:
            try:
                page.init_page()
            except Exception:
                import traceback
                error_detail = traceback.format_exc()
                self.subtitle_label.setText(error_detail)
                self.next_button.setEnabled(False)
                self.previous_button.setEnabled(False)
                print(u'Failed to init wizard page {}. Error:{}'.format(page, error_detail))
                # net_log.get_logger().error(u'Failed to init wizard page {}. Error:{}'.format(page, error_detail))
                page.initialized = True
                return
            page.initialized = True
        self._update_button(index)
        self._update_step(index)
        self._update_button_states()
        self.subtitle_label.setText(page.subtitle)

    def next_id(self):
        current_id = self.stacked_lay.currentIndex()
        if current_id + 1 == self.stacked_lay.count():
            return -1
        else:
            return current_id + 1

    @Slot(bool)
    def _update_button_states(self):
        flag = self.current_page().is_complete()
        self.next_button.setEnabled(flag)
