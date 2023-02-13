from typing import Any, Callable

import wx
from wx.adv import BitmapComboBox
import wx.lib.stattext as ST

import UI
from UI.KeySelectDialog import bcKeyButton
from BindFile import KeyBind
import wx.lib.stattext as ST

class ControlGroup(wx.StaticBoxSizer):

    def __init__(self, parent, page, label = '', width = 2, flexcols = [0]):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label = label)

        self.Page    = page

        self.InnerSizer = wx.FlexGridSizer(width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)
        self.Add(self.InnerSizer, 1, wx.ALL|wx.EXPAND, 10)

    def AddControl(self,
                   ctlType  : str = '',
                   ctlName  : str = '',
                   noLabel  : bool = False,
                   contents : Any = '',
                   tooltip  : str = '',
                   callback : Callable|None = None
        ):

        if not ctlName:
            wx.LogError(f"Tried to make a labeled control without a CtlName!")
            raise(Exception)

        Init      = self.Page.Init
        CtlParent = self.GetStaticBox()
        CtlLabel  = None

        padding = 0

        label = UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            # This ST.GenStaticText is so we can intercept clicks on it, but
            # the background color is wrong on Windows in a way I can't work out,
            # and clicks work on Windows anyway, so...
            if wx.Platform != '__WXMSW__':
                CtlLabel = ST.GenStaticText(CtlParent, -1, label + ':')
            else:
                CtlLabel = wx.StaticText(CtlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = bcKeyButton( CtlParent, -1, )
            control.SetLabel(Init[ctlName])
            # push context onto the button, we'll thank me later
            control.CtlName = ctlName
            control.Page    = self.Page
            control.Key     = Init[ctlName]

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = wx.ComboBox(
                CtlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif (ctlType == 'bmcombo') or (ctlType == "bmcombobox"):
            control = BitmapComboBox(
                CtlParent, -1, '',
                style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )
            for entry in contents:
                control.Append(*entry)
            index = control.FindString(Init[ctlName])
            if index == -1:
                control.SetValue(Init[ctlName])
            else:
                control.SetSelection(index)

        elif ctlType == ('text'):
            control = wx.TextCtrl(CtlParent, -1, Init[ctlName])

        elif ctlType == ('choice'):
            contents = contents if contents else []
            control = wx.Choice(CtlParent, -1, choices = contents)
            control.SetSelection(control.FindString(Init[ctlName]))
            if callback:
                control.Bind(wx.EVT_CHOICE, callback )

        elif ctlType == ('statictext'):
            control = wx.StaticText(CtlParent, -1, contents)

        elif ctlType == ('checkbox'):
            control = wx.CheckBox(CtlParent, -1, contents)
            control.SetValue(bool(Init[ctlName]))
            padding = 6
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback )

        elif ctlType == ('spinbox'):
            control = wx.SpinCtrl(CtlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('spinboxfractional'):
            control = wx.SpinCtrlDouble(CtlParent, inc = 0.05)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = wx.DirPickerCtrl(
                CtlParent, -1, Init[ctlName], Init[ctlName],
            )
        elif ctlType == ('colorpicker'):
            control = wx.ColourPickerCtrl( CtlParent, -1, contents)

        else:
            wx.LogError(f"Got a ctlType in ControlGroup that I don't know: {ctlType}")
            raise Exception

        # Pack'em in there
        if tooltip: control.SetToolTip( wx.ToolTip(tooltip) )

        control.CtlLabel = None
        if not noLabel and CtlLabel:
            CtlLabel.SetToolTip( wx.ToolTip(tooltip))
            self.InnerSizer.Add( CtlLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
            control.CtlLabel = CtlLabel
            CtlLabel.control = control

        # make checkboxes' labels click to check them
        if ctlType == ('checkbox') and control.CtlLabel:
            control.CtlLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        self.InnerSizer.Add( control, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, padding)
        self.Page.Ctrls[ctlName] = control

        self.Layout()
        return control

    def OnCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        fakeevt = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, cblabel.control.GetId())
        wx.PostEvent(cblabel.control, fakeevt)
        evt.Skip()

