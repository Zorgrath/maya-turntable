"""Turntable setup and creation tool.

A tool for creating turntables, with UI for the turntable's setup and for re-adjusting those settings. Can be launched from the shelf.
"""

import functools

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 

from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

# Get the mainWindow widget
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class CreateTurntable(QWidget):
    """Creates a tool for making turntables.

    Creates a window for a turntable creation tool. Sliders and spin 
    boxes control turntable settings. Push buttons create and readjust 
    turntables.

    Attributes:
        self.turntable_field (str): A field to link to the full path 
            name of the turntable sphere's control.
        self.camera_field (str): A field to link to the full path name 
            of the turntable camera's control.
        self.group_field (str): A field to link to the full path name 
            of the camera's group control.
        self.camera_distance (int): Used for storing the setting 
            controlling the camera's horizontal distance from the 
            turntable.
        self.camera_height (int): Used for storing the setting 
            controlling the camera's vertical position.
        self.angle_interval (double): Used for storing the setting 
            controlling how many degrees the camera rotates around the 
            turntable per frame.
    """

    def __init__(self, *args, **kwargs):
        """Initializes CreateTurntable.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(CreateTurntable, self).__init__(*args, **kwargs)
        # Connects and sets up the tool's window.
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName("CreateTurntable#")
        self.setWindowTitle("Create Turntable")

        # Variables for keeping the paths to the newest turntable 
        # objects.
        self.turntable_field = None
        self.camera_field = None
        self.group_field = None
        # Turntable's setting variables.  Set the initial UI values.  
        # Values updated with the "update_setting_values()" method.
        self.camera_distance = 5
        self.camera_height = 2
        self.angle_interval = 0.750000000000000
        
        self.initialize_UI()


    def initialize_UI(self):
        """Initializes UI widgets, layout and connects signals to slots."""
        # The "View" layout group for the section of UI that 
        # encompasses the camera's position in relation to the 
        # turntable.
        self.view_group_box = QGroupBox()
        self.view_group_box.setTitle("View")
        self.view_vertical_layout = QVBoxLayout(self.view_group_box)

        # UI section that controls "Camera Distance" to the turntable.
        self.distance_horizontal_layout = QHBoxLayout()
        # Keeps settings aligned.
        self.camera_distance_horizontal_spacer = QSpacerItem(
            34, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.distance_horizontal_layout.addItem(self.camera_distance_horizontal_spacer)
        # The QLabel widget for camera distance settings.
        self.camera_distance_label = QLabel(self.view_group_box)
        self.camera_distance_label.setText(" Camera Distance")
        self.camera_distance_label.setToolTip(
            "The horizontal distance between the render camera and the turntable's center")
        # QSpinBox widget for setting camera distance.  
        # Connected to "self.camera_distance_slider" widget.
        self.camera_distance_spin_box = QSpinBox(self.view_group_box)
        self.camera_distance_spin_box.setMinimumSize(QSize(70, 0))
        self.camera_distance_spin_box.setKeyboardTracking(False)
        self.camera_distance_spin_box.setMaximum(2147483647)
        self.camera_distance_spin_box.setValue(self.camera_distance)
        # The QSlider widget for setting camera distance.  
        # Connected to "self.camera_distance_spin_box" widget.
        self.camera_distance_slider = QSlider(self.view_group_box)
        self.camera_distance_slider.setMaximum(60)
        self.camera_distance_slider.setValue(self.camera_distance)
        self.camera_distance_slider.setOrientation(Qt.Horizontal)
        # Groups all "Camera Distance" widgets and adds them to the 
        # "View" layout group.
        self.distance_horizontal_layout.addWidget(self.camera_distance_label)
        self.distance_horizontal_layout.addWidget(self.camera_distance_spin_box)
        self.distance_horizontal_layout.addWidget(self.camera_distance_slider)
        self.view_vertical_layout.addLayout(self.distance_horizontal_layout)

        # UI section that controls "Camera Height" along the Y-axis.
        self.height_horizontal_layout = QHBoxLayout()
        # Keeps settings aligned.
        self.camera_height_horizontal_spacer = QSpacerItem(
            46, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.height_horizontal_layout.addItem(self.camera_height_horizontal_spacer)
        # The QLabel widget for camera height settings.
        self.camera_height_label = QLabel(self.view_group_box)
        self.camera_height_label.setText(" Camera Height")
        self.camera_height_label.setToolTip(
            "The Y coordinates for the turntable's render camera")
        # QSpinBox widget for setting camera height.  
        # Connected to "self.camera_height_slider" widget.
        self.camera_height_spin_box = QSpinBox(self.view_group_box)
        self.camera_height_spin_box.setMinimumSize(QSize(70, 0))
        self.camera_height_spin_box.setKeyboardTracking(False)
        self.camera_height_spin_box.setMinimum(-2147483647)
        self.camera_height_spin_box.setMaximum(2147483647)
        self.camera_height_spin_box.setValue(self.camera_height)
        # The QSlider widget for setting camera height.  
        # Connected to "self.camera_height_spin_box" widget.
        self.camera_height_slider = QSlider(self.view_group_box)
        self.camera_height_slider.setMinimum(-20)
        self.camera_height_slider.setMaximum(40)
        self.camera_height_slider.setValue(self.camera_height)
        self.camera_height_slider.setOrientation(Qt.Horizontal)
        # Groups all "Camera Height" widgets and adds them to the 
        # "View" layout group.
        self.height_horizontal_layout.addWidget(self.camera_height_label)
        self.height_horizontal_layout.addWidget(self.camera_height_spin_box)
        self.height_horizontal_layout.addWidget(self.camera_height_slider)
        self.view_vertical_layout.addLayout(self.height_horizontal_layout)

        # The "Rotation" layout group for the section of UI that 
        # encompasses the camera's rotation around the turntable.
        self.rotation_group_box = QGroupBox()
        self.rotation_group_box.setTitle("Rotation")
        self.rotation_horizontal_layout = QHBoxLayout(self.rotation_group_box)
        # The QLabel widget for rotation angle interval settings.
        self.turntable_rotation_label = QLabel(self.rotation_group_box)
        self.turntable_rotation_label.setText(" Turntable Angle Interval")
        self.turntable_rotation_label.setToolTip(
            "How many degrees the render camera rotates around the turntable per frame")
        # QDoubleSpinBox widget for setting angle intervals per frame.
        self.turntable_rotation_double_spin_box = QDoubleSpinBox(self.rotation_group_box)
        self.turntable_rotation_double_spin_box.setMinimumSize(QSize(70, 0))
        self.turntable_rotation_double_spin_box.setSuffix(u"\u00b0")
        self.turntable_rotation_double_spin_box.setMinimum(-90.000000000000000)
        self.turntable_rotation_double_spin_box.setMaximum(90.000000000000000)
        self.turntable_rotation_double_spin_box.setSingleStep(0.250000000000000)
        self.turntable_rotation_double_spin_box.setValue(self.angle_interval)
        # Groups all "Rotation" widgets and adds them to the 
        # "Rotation" layout group.
        self.rotation_horizontal_layout.addWidget(self.turntable_rotation_label)
        self.rotation_horizontal_layout.addWidget(self.turntable_rotation_double_spin_box)
        # Keeps settings aligned.
        self.turntable_rotation_horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.rotation_horizontal_layout.addItem(self.turntable_rotation_horizontal_spacer)
        
        # Keeps settings aligned.
        self.input_button_vertical_spacer = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # The "Button" layout group for the section of UI that 
        # controls creating, and apply setting changes to, turntables.
        self.buttons_horizontal_layout = QHBoxLayout()
        # Keeps settings aligned.
        self.buttons_horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttons_horizontal_layout.addItem(self.buttons_horizontal_spacer)
        # The QPushButton widget for creating new turntables.
        self.create_push_button = QPushButton(self)
        self.create_push_button.setText("Create")
        # The QPushButton widget for apply any setting changes to the 
        # most recently created turntable.
        self.apply_push_button = QPushButton(self)
        self.apply_push_button.setText("Apply")
        self.apply_push_button.setEnabled(False)
        # The QPushButton widget for closing the tool window.
        self.close_push_button = QPushButton(self)
        self.close_push_button.setText("Close")
        # Groups all "Button" widgets and adds them to the 
        # "Button" layout group.
        self.buttons_horizontal_layout.addWidget(self.create_push_button)
        self.buttons_horizontal_layout.addWidget(self.apply_push_button)
        self.buttons_horizontal_layout.addWidget(self.close_push_button)

        # The tool's "Master" layout, to which all other layouts and 
        # widgets get added to.
        layout = QVBoxLayout()
        layout.addWidget(self.view_group_box)
        layout.addWidget(self.rotation_group_box)
        layout.addItem(self.input_button_vertical_spacer)
        layout.addLayout(self.buttons_horizontal_layout)
        self.setLayout(layout)

        # Use "functools.partial()" to dynamically construct a function
        # with additional parameters.  Allows the QSlider's range to 
        # increase with the value it shares with the QSpinBox it is 
        # connected to.
        on_change_distance_spin_box_func = functools.partial(
            self.on_value_changed, spin_box=self.camera_distance_spin_box, 
            slider=self.camera_distance_slider)
        self.camera_distance_spin_box.valueChanged.connect(on_change_distance_spin_box_func)
        
        on_change_height_spin_box_func = functools.partial(
            self.on_value_changed, spin_box=self.camera_height_spin_box, 
            slider=self.camera_height_slider)
        self.camera_height_spin_box.valueChanged.connect(on_change_height_spin_box_func)

        # Connects the settting's QSpinBoxs with their associated 
        # QSlider and vice versa, linking each pairs value.
        self.camera_distance_spin_box.valueChanged.connect(self.camera_distance_slider.setValue)
        self.camera_distance_slider.valueChanged.connect(self.camera_distance_spin_box.setValue)
        self.camera_height_spin_box.valueChanged.connect(self.camera_height_slider.setValue)
        self.camera_height_slider.valueChanged.connect(self.camera_height_spin_box.setValue)

        # Exits the tool when the "Close" button is pressed.
        self.close_push_button.pressed.connect(self.close)
        # Creates a new turntable using the tools current settings.  
        # Also enables the "Apply" button.
        self.create_push_button.clicked.connect(self.create_button_on_clicked)
        # Applies the tools current settings to the most recently 
        # created turntable.
        self.apply_push_button.clicked.connect(self.apply_button_on_clicked)
        # ____
        QMetaObject.connectSlotsByName(self)
        
    def on_value_changed(self, spinner_value, spin_box:QSpinBox, slider:QSlider):
        """Increases the range of a slider's current range limit.

        Adjusts the maximum range of a slider when the linked value of 
        the spin box connected to it nears or surpasses the slider's 
        maximum range.  Lowers the minimum range of sliders with 
        negative minimum ranges when the linked value of the spin box 
        connected to it nears or surpasses the slider's minimum range.
        
        Args:
            spinner_value (int): The value passed from the connected 
                spin box.
            spin_box (:QSpinBox): The triggering spin box widget.
            slider (QSlider): The slider connected to the spin_box.
        """
        # Adjust how near to the range's limit the value needs to 
        # reach, or surpass, to cause the range to increase.
        buffer = 0.98
        increment = 1.07  # Adjusts how much the range increase by.

        # Checks to see wether the changed value is close to QSlider's 
        # range maximum.
        if spinner_value >= (slider.maximum()*buffer):
            max_spin = spinner_value * increment  # New max range.
            # Limits max range if it exceeds what the QSpinBox allows.
            if max_spin >= spin_box.maximum():
                max_spin = spin_box.maximum()
            # Sets the QSlider's new maximum range and updates the UI.
            slider.setRange(slider.minimum(), max_spin)
            slider.update()

        # Checks to see wether the QSlider can be negative and if the 
        # changed value is close to QSlider's range minimum.
        if spin_box.minimum() < 0 and spinner_value <= (slider.minimum()*buffer):
            negative_spin = spinner_value * increment  # New min range.
            # Limits min range if it exceeds what the QSpinBox allows.
            if negative_spin <= spin_box.minimum():
                negative_spin = spin_box.minimum()
            # Sets the QSlider's new minimum range and updates the UI.
            slider.setRange(negative_spin, slider.maximum())
            slider.update()

    def update_setting_values(self):
        """Updates the setting's variables."""
        self.camera_distance = self.camera_distance_spin_box.value()
        self.camera_height = self.camera_height_spin_box.value()
        self.angle_interval = self.turntable_rotation_double_spin_box.value()

    def create_button_on_clicked(self):
        """Creates the turntable and camera."""
        # Makes sure the setting variables are up to date.
        self.update_setting_values()
        # Creates a sphere to be the turntable center and sets it's 
        # field to always link to that sphere.
        turntable_transform = cmds.polySphere(n="pTurntableSphere#")[0]
        self.turntable_field = cmds.nameField(object=turntable_transform)
        # Get's the name of the turntable sphere from its field.
        turntable_name = cmds.nameField(self.turntable_field, query=True, object=True)

        # Creates a camera positioned using the settings and sets it's 
        # field to always link to that camera.
        camera_transform = cmds.camera(n="turntableCamera#", 
                                       p=[0, self.camera_height, 
                                          self.camera_distance])[0]
        self.camera_field = cmds.nameField(object=camera_transform)
        # Get's the name of the camera from its field.
        camera_name = cmds.nameField(self.camera_field, query=True, object=True)

        # Creates an empty group and sets it's field to always link to 
        # that group.
        rotator_group = cmds.group(em=True, n="rotationGroup#")
        self.group_field = cmds.nameField(object=rotator_group)
        # Get's the name of the group from its field.
        rotator_name = cmds.nameField(self.group_field, query=True, object=True)

        # Group's the camera, sphere and group together.
        cmds.parent(camera_name, rotator_name, relative=True)
        cmds.parent(rotator_name, turntable_name, relative=True)
        # Get's the name of the group from its field again, because it 
        # changes from parenting.
        rotator_name = cmds.nameField(self.group_field, query=True, object=True)

        # Passes the group to be animated.
        self.set_rotation(rotator_name)
        # Enables the "Apply" button and updates the UI.
        self.apply_push_button.setEnabled(True)
        self.apply_push_button.update()

    def apply_button_on_clicked(self):
        """Applies setting changes to the newest turntable."""
        # Makes sure the setting variables are up to date.
        self.update_setting_values()
        # Get's the names of the newest group and camera from their 
        # fields.
        rotator_name = cmds.nameField(self.group_field, query=True, object=True)
        camera_name = cmds.nameField(self.camera_field, query=True, object=True)
        if cmds.objExists(camera_name) and cmds.objExists(rotator_name):
            # Applies any changes to the settings to the most recently 
            # created turntable if the camera and group exist.
            cmds.setAttr("%s.translateY"%camera_name, self.camera_height)
            cmds.setAttr("%s.translateZ"%camera_name, self.camera_distance)
            self.set_rotation(rotator_name)
        else:
            # Creates a new turntable if the camera or group don't exist.
            self.create_button_on_clicked()

    def set_rotation(self, rotator):
        """Sets the camera's rotation animation.
        
        Args:
            rotator (str): The name group of the group that the 
                turntable's camera is a child of.
        """
        start_time = cmds.playbackOptions(query=True, minTime=True)
        # The number of frames required for the camera to rotate a 
        # full 360 degrees.
        end_time = ((360-self.angle_interval)/self.angle_interval) + (start_time-1)
        # Set the length of the animation to be exactly one rotation.
        cmds.playbackOptions(maxTime=end_time)
        if cmds.playbackOptions(query=True, animationEndTime=True) < end_time:
            cmds.playbackOptions(animationEndTime=end_time)
        #  Sets the keys for the rotation animation.
        cmds.cutKey(rotator, time=(start_time, end_time), attribute="rotateY")
        cmds.setKeyframe(rotator, time=start_time, attribute="rotateY", value=0)
        cmds.setKeyframe(rotator, time=end_time, attribute="rotateY", 
                         value=(end_time * self.angle_interval))
        # Makes the animation's rotation speed constant.
        cmds.selectKey(rotator, time=(start_time, end_time), attribute="rotateY", keyframe=True)
        cmds.keyTangent(inTangentType="linear", outTangentType="linear")
            
def main():
    ui = CreateTurntable()
    ui.show()
    return ui
    
if __name__ == "__main__":
    main()
