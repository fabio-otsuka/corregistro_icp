class NeuronavigationTools(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        default_colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_MENUBAR)
        self.SetBackgroundColour(default_colour)

        self.SetAutoLayout(1)

        self.__bind_events()
        self.aux_img_ref1 = 0
        self.aux_img_ref2 = 0
        self.aux_img_ref3 = 0
        self.aux_img__T_ref = 0
        self.aux_trck_ref1 = 0
        self.aux_trck_ref2 = 0
        self.aux_trck_ref3 = 0
        self.aux_trck1 = 0
        self.aux_trck2 = 0
        self.aux_trck3 = 0
        self.a = 0, 0, 0
        self.coord1a = (0, 0, 0)
        self.coord2a = (0, 0, 0)
        self.coord3a = (0, 0, 0)
        self.coord1b = (0, 0, 0)
        self.coord2b = (0, 0, 0)
        self.coord3b = (0, 0, 0)
        self.correg = None
        self.filename = None
        self.c1 = None
        self.tracker_id = const.DEFAULT_TRACKER
        self.ref_mode_id = const.DEFAULT_REF_MODE

        self.trk_init = None

        #Combo Box
        self.choice_tracker = wx.ComboBox(self, -1, "",
                                     choices = const.TRACKER, style = wx.CB_DROPDOWN|wx.CB_READONLY)
        self.choice_tracker.SetSelection(const.DEFAULT_TRACKER)
        self.choice_tracker.Bind(wx.EVT_COMBOBOX, self.OnChoiceTracker)

        tooltip = wx.ToolTip(_("Choose the navigation reference mode"))
        self.choice_ref_mode = wx.ComboBox(self, -1, "",
                                     choices = const.REF_MODE, style = wx.CB_DROPDOWN|wx.CB_READONLY)
        self.choice_ref_mode.SetSelection(const.DEFAULT_REF_MODE)
        self.choice_ref_mode.SetToolTip(tooltip)
        self.choice_ref_mode.Bind(wx.EVT_COMBOBOX, self.OnChoiceRefMode)

        #Toggle Buttons for ref images
        tooltip = wx.ToolTip(_("Select left auricular tragus at image"))
        self.button_img_ref1 = wx.ToggleButton(self, IR1, label = _('LTI'), size = wx.Size(30,23))
        self.button_img_ref1.SetToolTip(tooltip)
        self.button_img_ref1.Bind(wx.EVT_TOGGLEBUTTON, self.Img_Ref_ToggleButton1)

        tooltip = wx.ToolTip(_("Select right auricular tragus at image"))
        self.button_img_ref2 = wx.ToggleButton(self, IR2, label = _('RTI'), size = wx.Size(30,23))
        self.button_img_ref2.SetToolTip(tooltip)
        self.button_img_ref2.Bind(wx.EVT_TOGGLEBUTTON, self.Img_Ref_ToggleButton2)

        tooltip = wx.ToolTip(_("Select nasion at image"))
        self.button_img_ref3 = wx.ToggleButton(self, IR3, label = _('NI'), size = wx.Size(30,23))
        self.button_img_ref3.SetToolTip(tooltip)
        self.button_img_ref3.Bind(wx.EVT_TOGGLEBUTTON, self.Img_Ref_ToggleButton3)

        #self.button_img_inio = wx.Button(self, INO, label='INO', size=wx.Size(30, 23))
        tooltip = wx.ToolTip(_("Select target point at image for target registration error calculation"))
        self.button_img_T = wx.ToggleButton(self, T, label = 'T', size = wx.Size(30,23))
        self.button_img_T.SetToolTip(tooltip)
        self.button_img_T.Bind(wx.EVT_TOGGLEBUTTON, self.Img_T_ToggleButton)

        #Buttons for ref tracker
        tooltip = wx.ToolTip(_("Select left auricular tragus with spatial tracker"))
        self.button_trck_ref1 = wx.Button(self, TR1, label = _('LTT'), size = wx.Size(30,23))
        self.button_trck_ref1.SetToolTip(tooltip)
        tooltip = wx.ToolTip(_("Select right auricular tragus with spatial tracker"))
        self.button_trck_ref2 = wx.Button(self, TR2, label = _('RTT'), size = wx.Size(30,23))
        self.button_trck_ref2.SetToolTip(tooltip)
        tooltip = wx.ToolTip(_("Select nasion with spatial tracker"))
        self.button_trck_ref3 = wx.Button(self, TR3, label = _('NT'), size = wx.Size(30,23))
        self.button_trck_ref3.SetToolTip(tooltip)

        #Error text box
        self.button_crg = wx.TextCtrl(self, value="")
        self.button_crg.SetEditable(0)
        self.Bind(wx.EVT_BUTTON, self.Buttons)

        tooltip = wx.ToolTip(_("Start neuronavigation"))
        self.button_neuronavigate = wx.ToggleButton(self, Neuronavigate, _("Neuronavigate"))
        self.button_neuronavigate.SetToolTip(tooltip)
        self.button_neuronavigate.Bind(wx.EVT_TOGGLEBUTTON, self.Neuronavigate_ToggleButton)

        self.numCtrl1I = wx.lib.masked.numctrl.NumCtrl(
           name='numCtrl1I', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2I = wx.lib.masked.numctrl.NumCtrl(
           name='numCtrl2I', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3I = wx.lib.masked.numctrl.NumCtrl(
           name='numCtrl3I', parent=self, integerWidth = 4, fractionWidth = 1)

        self.numCtrl1a = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1a', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2a = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2a', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3a = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3a', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl1b = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1b', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2b = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2b', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3b = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3b', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl1c = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1c', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2c = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2c', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3c = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3c', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl1d = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1d', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2d = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2d', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3d = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3d', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl1e = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1e', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2e = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2e', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3e = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3e', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl1f = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl1f', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl2f = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl2f', parent=self, integerWidth = 4, fractionWidth = 1)
        self.numCtrl3f = wx.lib.masked.numctrl.NumCtrl(
            name='numCtrl3f', parent=self, integerWidth = 4, fractionWidth = 1)

        self.numCtrl1d.SetEditable(False)
        self.numCtrl2d.SetEditable(False)
        self.numCtrl3d.SetEditable(False)
        self.numCtrl1e.SetEditable(False)
        self.numCtrl2e.SetEditable(False)
        self.numCtrl3e.SetEditable(False)
        self.numCtrl1f.SetEditable(False)
        self.numCtrl2f.SetEditable(False)
        self.numCtrl3f.SetEditable(False)

        choice_sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
        choice_sizer.AddMany([ (self.choice_tracker, wx.LEFT),
                                (self.choice_ref_mode, wx.RIGHT)])

        RefImg_sizer1 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefImg_sizer1.AddMany([ (self.button_img_ref1),
                                (self.numCtrl1a),
                                (self.numCtrl2a),
                                (self.numCtrl3a)])

        RefImg_sizer2 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefImg_sizer2.AddMany([ (self.button_img_ref2),
                                (self.numCtrl1b),
                                (self.numCtrl2b),
                                (self.numCtrl3b)])

        RefImg_sizer3 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefImg_sizer3.AddMany([ (self.button_img_ref3),
                                (self.numCtrl1c),
                                (self.numCtrl2c),
                                (self.numCtrl3c)])

        RefPlh_sizer1 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefPlh_sizer1.AddMany([ (self.button_trck_ref1, 0, wx.GROW|wx.EXPAND),
                                (self.numCtrl1d, wx.RIGHT),
                                (self.numCtrl2d),
                                (self.numCtrl3d, wx.LEFT)])

        RefPlh_sizer2 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefPlh_sizer2.AddMany([ (self.button_trck_ref2, 0, wx.GROW|wx.EXPAND),
                                (self.numCtrl1e, 0, wx.RIGHT),
                                (self.numCtrl2e),
                                (self.numCtrl3e, 0, wx.LEFT)])

        RefPlh_sizer3 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        RefPlh_sizer3.AddMany([ (self.button_trck_ref3, 0, wx.GROW|wx.EXPAND),
                                (self.numCtrl1f, wx.RIGHT),
                                (self.numCtrl2f),
                                (self.numCtrl3f, wx.LEFT)])

        line3 = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
        line3.AddMany([(self.button_img_T),
                      (self.numCtrl1I),
                      (self.numCtrl2I),
                      (self.numCtrl3I)])

        Buttons_sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
        Buttons_sizer.AddMany([(self.button_crg, wx.LEFT|wx.RIGHT),
                               (self.button_neuronavigate, wx.LEFT|wx.RIGHT)])

        Ref_sizer = wx.FlexGridSizer(rows=9, cols=1, hgap=5, vgap=5)
        Ref_sizer.AddGrowableCol(0, 1)
        Ref_sizer.AddGrowableRow(0, 1)
        Ref_sizer.AddGrowableRow(1, 1)
        Ref_sizer.AddGrowableRow(2, 1)
        Ref_sizer.AddGrowableRow(3, 1)
        Ref_sizer.AddGrowableRow(4, 1)
        Ref_sizer.AddGrowableRow(5, 1)
        Ref_sizer.AddGrowableRow(6, 1)
        Ref_sizer.AddGrowableRow(7, 1)
        Ref_sizer.AddGrowableRow(8, 1)
        Ref_sizer.SetFlexibleDirection(wx.BOTH)
        Ref_sizer.AddMany([ (choice_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefImg_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefImg_sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefImg_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefPlh_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefPlh_sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (RefPlh_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (line3, 0,wx.ALIGN_CENTER_HORIZONTAL),
                            (Buttons_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)])

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(Ref_sizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.sizer = main_sizer
        self.SetSizer(main_sizer)
        self.Fit()

    def __bind_events(self):
        Publisher.subscribe(self.__update_points_img, 'Update cross position')
        Publisher.subscribe(self.__update_points_trck, 'Update tracker position')
        Publisher.subscribe(self.__load_points_img, 'Load Fiducial')

    def __update_points_img(self, pubsub_evt):
        x, y, z = pubsub_evt.data
        self.a = x, y, z
        if self.aux_img_ref1 == 0:
            self.numCtrl1a.SetValue(x)
            self.numCtrl2a.SetValue(y)
            self.numCtrl3a.SetValue(z)
        if self.aux_img_ref2 == 0:
            self.numCtrl1b.SetValue(x)
            self.numCtrl2b.SetValue(y)
            self.numCtrl3b.SetValue(z)
        if self.aux_img_ref3 == 0:
            self.numCtrl1c.SetValue(x)
            self.numCtrl2c.SetValue(y)
            self.numCtrl3c.SetValue(z)
        if self.aux_img__T_ref == 0:
           self.numCtrl1I.SetValue(x)
           self.numCtrl2I.SetValue(y)
           self.numCtrl3I.SetValue(z)

    def __update_points_trck(self, pubsub_evt):
        coord = pubsub_evt.data
        if self.aux_trck_ref1 == 1:
            self.numCtrl1d.SetValue(coord[0])
            self.numCtrl2d.SetValue(coord[1])
            self.numCtrl3d.SetValue(coord[2])
            self.aux_trck1 = 1
            self.aux_trck_ref1 = 0
        if self.aux_trck_ref2 == 1:
            self.numCtrl1e.SetValue(coord[0])
            self.numCtrl2e.SetValue(coord[1])
            self.numCtrl3e.SetValue(coord[2])
            self.aux_trck2 = 1
            self.aux_trck_ref2 = 0
        if self.aux_trck_ref3 == 1:
            self.numCtrl1f.SetValue(coord[0])
            self.numCtrl2f.SetValue(coord[1])
            self.numCtrl3f.SetValue(coord[2])
            self.aux_trck3 = 1
            self.aux_trck_ref3 = 0

    def __load_points_img(self, pubsub_evt):
        load = pubsub_evt.data[0]
        coord = pubsub_evt.data[1]
        if load == "LTI":
            self.Load_Ref_LTI(coord)
        elif load == "RTI":
            self.Load_Ref_RTI(coord)
        elif load == "NI":
            self.Load_Ref_NI(coord)

    def Load_Ref_LTI(self,coord):
        img_id = self.button_img_ref1.GetValue()
        x, y, z = coord
        if img_id == False:
            self.numCtrl1a.SetValue(x)
            self.numCtrl2a.SetValue(y)
            self.numCtrl3a.SetValue(z)
            self.coord1a = x, y, z
            self.button_img_ref1.SetValue(True)
            self.aux_img_ref1 = 1
        else:
            None

    def Load_Ref_RTI(self,coord):
        img_id = self.button_img_ref2.GetValue()
        x, y, z = coord
        if img_id == False:
            self.numCtrl1b.SetValue(x)
            self.numCtrl2b.SetValue(y)
            self.numCtrl3b.SetValue(z)
            self.coord2a = x, y, z
            self.button_img_ref2.SetValue(True)
            self.aux_img_ref2 = 1
        else:
            None

    def Load_Ref_NI(self,coord):
        img_id = self.button_img_ref3.GetValue()
        x, y, z = coord
        if img_id == False:
            self.numCtrl1c.SetValue(x)
            self.numCtrl2c.SetValue(y)
            self.numCtrl3c.SetValue(z)
            self.coord3a = x, y, z
            self.button_img_ref3.SetValue(True)
            self.aux_img_ref3 = 1
        else:
            None

    def Buttons(self, evt):
        id = evt.GetId()
        x, y, z = self.a
        if id == TR1:
            if self.trk_init and (self.tracker_id != 0):
                self.aux_trck_ref1 = 1
                self.coord1b = dco.Coordinates(self.trk_init, self.tracker_id, self.ref_mode_id).Returns()
                coord = self.coord1b[0:3]
            else:
                dlg.TrackerNotConnected(self.tracker_id)

        elif id == TR2:
            if self.trk_init and (self.tracker_id != 0):
                self.aux_trck_ref2 = 1
                self.coord2b = dco.Coordinates(self.trk_init, self.tracker_id, self.ref_mode_id).Returns()
                coord = self.coord2b[0:3]
            else:
                dlg.TrackerNotConnected(self.tracker_id)
        elif id == TR3:
            if self.trk_init and (self.tracker_id != 0):
                self.aux_trck_ref3 = 1
                self.coord3b = dco.Coordinates(self.trk_init, self.tracker_id, self.ref_mode_id).Returns()
                coord = self.coord3b[0:3]
            else:
                dlg.TrackerNotConnected(self.tracker_id)

        if self.aux_trck_ref1 == 1 or self.aux_trck_ref2 == 1 or self.aux_trck_ref3 == 1:
            Publisher.sendMessage('Update tracker position', coord)

    def Img_Ref_ToggleButton1(self, evt):
        img_id = self.button_img_ref1.GetValue()
        #this fixed points are from dicom2 exam
        x, y, z = self.a
#        x, y, z = 201.1, 113.3, 31.5
        if img_id == True:
            #This condition allows the user writes the image coords
            if self.numCtrl1a.GetValue() != round(x, 1) or self.numCtrl2a.GetValue() != round(y,1) or self.numCtrl3a.GetValue() != round(z, 1):
                self.coord1a = self.numCtrl1a.GetValue(), self.numCtrl2a.GetValue(), self.numCtrl3a.GetValue()
                Publisher.sendMessage('Set camera in volume for Navigation', self.coord1a)
                Publisher.sendMessage('Co-registered Points', self.coord1a)
                self.aux_img_ref1 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord1a, "LTI"))
            else:
                self.coord1a = x, y, z
                self.aux_img_ref1 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord1a, "LTI"))

        elif img_id == False:
            self.aux_img_ref1 = 0
            self.coord1a = (0, 0, 0)
            self.numCtrl1a.SetValue(x)
            self.numCtrl2a.SetValue(y)
            self.numCtrl3a.SetValue(z)
            Publisher.sendMessage("Delete fiducial marker", "LTI")

    def Img_Ref_ToggleButton2(self, evt):
        img_id = self.button_img_ref2.GetValue()
        #this fixed points are from dicom2 exam
        x, y, z = self.a
#        x, y, z = 50.4, 113.3, 30.0
        if img_id == True:
            #This condition allows the user writes the image coords
            if self.numCtrl1b.GetValue() != round(x, 1) or self.numCtrl2b.GetValue() != round(y,1) or self.numCtrl3b.GetValue() != round(z, 1):
                self.coord2a = self.numCtrl1b.GetValue(), self.numCtrl2b.GetValue(), self.numCtrl3b.GetValue()
                Publisher.sendMessage('Set camera in volume for Navigation', self.coord2a)
                Publisher.sendMessage('Co-registered Points', self.coord2a)
                self.aux_img_ref2 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord2a, "RTI"))
            else:
                self.coord2a = x, y, z
                self.aux_img_ref2 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord2a, "RTI"))

        elif img_id == False:
            self.aux_img_ref2 = 0
            self.coord2a = (0, 0, 0)
            self.numCtrl1b.SetValue(x)
            self.numCtrl2b.SetValue(y)
            self.numCtrl3b.SetValue(z)
            Publisher.sendMessage("Delete fiducial marker", "RTI")

    def Img_Ref_ToggleButton3(self, evt):
        img_id = self.button_img_ref3.GetValue()
        #this fixed points are from dicom2 exam
        x, y, z = self.a
#        x, y, z = 123.4, 207.4, 67.5
        if img_id == True:
            #This condition allows the user writes the image coords
            if self.numCtrl1c.GetValue() != round(x, 1) or self.numCtrl2c.GetValue() != round(y,1) or self.numCtrl3c.GetValue() != round(z, 1):
                self.coord3a = self.numCtrl1c.GetValue(), self.numCtrl2c.GetValue(), self.numCtrl3c.GetValue()
                Publisher.sendMessage('Set camera in volume for Navigation', self.coord3a)
                Publisher.sendMessage('Co-registered Points', self.coord3a)
                self.aux_img_ref3 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord3a, "NI"))
            else:
                self.coord3a = x, y, z
                self.aux_img_ref3 = 1
                Publisher.sendMessage("Create fiducial markers", (self.coord3a, "NI"))

        elif img_id == False:
            self.aux_img_ref3 = 0
            self.coord3a = (0, 0, 0)
            self.numCtrl1c.SetValue(x)
            self.numCtrl2c.SetValue(y)
            self.numCtrl3c.SetValue(z)
            Publisher.sendMessage("Delete fiducial marker", "NI")

    def Img_T_ToggleButton(self, evt):
           img_id = self.button_img_T.GetValue()
           x, y, z = self.a
           if img_id == True:
               # This condition allows the user writes the image coords
               if self.numCtrl1I.GetValue() != round(x,1) or self.numCtrl2I.GetValue() != round(y,1) or self.numCtrl3I.GetValue() != round(z,1):
                   self.img_T = self.numCtrl1I.GetValue(), self.numCtrl2I.GetValue(), self.numCtrl3I.GetValue()
                   Publisher.sendMessage('Set camera in volume for Navigation', self.img_T)
                   Publisher.sendMessage('Co-registered Points', self.img_T)
                   self.aux_img__T_ref = 1
                   self.coordT = np.array([self.numCtrl1I.GetValue(),self.numCtrl2I.GetValue(),self.numCtrl3I.GetValue()])
               else:
                   self.img_T = x, y, z
                   self.aux_img__T_ref = 1
                   self.coordT = np.array([x,y,z])
           elif img_id == False:
               self.aux_img__T_ref = 0
               self.img_T = (0, 0, 0)
               self.numCtrl1I.SetValue(x)
               self.numCtrl2I.SetValue(y)
               self.numCtrl3I.SetValue(z)

    def Neuronavigate_ToggleButton(self, evt):
        nav_id = self.button_neuronavigate.GetValue()
        if nav_id == True:
            if self.aux_trck1 and self.aux_trck2 and self.aux_trck3 and self.aux_img_ref1 and self.aux_img_ref2 and self.aux_img_ref3:
                tooltip = wx.ToolTip(_("Stop neuronavigation"))
                self.button_neuronavigate.SetToolTip(tooltip)
                self.Enable_Disable_buttons(False)
                self.Corregistration()
                bases = self.Minv, self.N, self.q1, self.q2
                tracker_mode = self.trk_init, self.tracker_id, self.ref_mode_id
                self.Calculate_FRE()
                self.correg = dcr.Corregistration(bases, nav_id, tracker_mode)
            else:
                dlg.InvalidReferences()
                self.button_neuronavigate.SetValue(False)
        elif nav_id == False:
            self.Enable_Disable_buttons(True)
            tooltip = wx.ToolTip(_("Start neuronavigation"))
            self.button_neuronavigate.SetToolTip(tooltip)
            self.correg.stop()

    def Enable_Disable_buttons(self,status):
        self.choice_ref_mode.Enable(status)
        self.choice_tracker.Enable(status)
        self.button_img_ref1.Enable(status)
        self.button_img_ref2.Enable(status)
        self.button_img_ref3.Enable(status)

    def Calculate_FRE(self):

        p1 = np.matrix([[self.coord1b[0]],[self.coord1b[1]],[self.coord1b[2]]])
        p2 = np.matrix([[self.coord2b[0]],[self.coord2b[1]],[self.coord2b[2]]])
        p3 = np.matrix([[self.coord3b[0]],[self.coord3b[1]],[self.coord3b[2]]])

        img1 = self.q1 + (self.Minv * self.N) * (p1 - self.q2)
        img2 = self.q1 + (self.Minv * self.N) * (p2 - self.q2)
        img3 = self.q1 + (self.Minv * self.N) * (p3 - self.q2)

        ED1=np.sqrt((((img1[0]-self.coord1a[0])**2) + ((img1[1]-self.coord1a[1])**2) +((img1[2]-self.coord1a[2])**2)))
        ED2=np.sqrt((((img2[0]-self.coord2a[0])**2) + ((img2[1]-self.coord2a[1])**2) +((img2[2]-self.coord2a[2])**2)))
        ED3=np.sqrt((((img3[0]-self.coord3a[0])**2) + ((img3[1]-self.coord3a[1])**2) +((img3[2]-self.coord3a[2])**2)))

        FRE = float(np.sqrt((ED1**2 + ED2**2 + ED3**2)/3))

        #TRE calculation
        # if self.aux_img__T_ref == 1:
        #     N1 = ([self.coord1a[0], self.coord2a[0], self.coord3a[0]])
        #     norm1 = [float(i) / sum(N1) for i in N1]
        #     N2 = ([self.coord1a[1], self.coord2a[1], self.coord3a[1]])
        #     norm2 = [float(i) / sum(N2) for i in N2]
        #     N3 = ([self.coord1a[2], self.coord2a[2], self.coord3a[2]])
        #     norm3 = [float(i) / sum(N3) for i in N3]
        #
        #     plhT = np.matrix([[self.coordT[0]], [self.coordT[1]], [self.coordT[2]]])
        #     #imgT = self.q1 + (self.Minv * self.N) * (plhT - self.q2)
        #     #imgT = np.array([float(imgT[0]), float(imgT[1]), float(imgT[2])])
        #     centroid = np.array([(self.coord1a[0] + self.coord2a[0] + self.coord3a[0]) / 3, (self.coord1a[1] + self.coord2a[1] + self.coord3a[1]) / 3, (self.coord1a[2] + self.coord2a[2] + self.coord3a[2]) / 3])
        #     #Difference between the target point (after coregister) with the fiducials centroid
        #     #dif_vector = imgT - centroid
        #     dif_vector = plhT - centroid
        #
        #     er1 = np.linalg.norm(np.cross(norm1, dif_vector))
        #     er2 = np.linalg.norm(np.cross(norm2, dif_vector))
        #     er3 = np.linalg.norm(np.cross(norm3, dif_vector))
        #
        #     err1 = err2 = err3 = 0
        #
        #     for i in range(0, 3):
        #         # Difference between each fiducial with the fiducials centroid
        #         diff_vector = [self.coord1a[i] - centroid[0], self.coord2a[i] - centroid[0], self.coord3a[i] - centroid[0]]
        #
        #         err1 += (np.linalg.norm(np.cross(norm1, diff_vector)))** 2
        #         err2 += (np.linalg.norm(np.cross(norm2, diff_vector)))** 2
        #         err3 += (np.linalg.norm(np.cross(norm3, diff_vector)))** 2
        #
        #     f1 = np.sqrt(err1 / 3)
        #     f2 = np.sqrt(err2 / 3)
        #     f3 = np.sqrt(err3 / 3)
        #
        #     SUM = ((er1 ** 2) / (f1 ** 2)) + ((er2 ** 2) / (f2 ** 2)) + ((er3 ** 2) / (f3 ** 2))
        #     TREf = np.sqrt((FRE ** 2) * (1 + (SUM / 3)))
        #
        #     self.button_crg.SetValue("FRE: " + str(round(FRE, 2))+" TRE: " + str(round(TREf, 2)))
        #
        # else:
        #     self.button_crg.SetValue("FRE: " + str(round(FRE, 2)))
        self.button_crg.SetValue("FRE: " + str(round(FRE, 2)))
        if FRE <= 3:
            self.button_crg.SetBackgroundColour('GREEN')
        else:
            self.button_crg.SetBackgroundColour('RED')

    def OnChoiceTracker(self, evt):
        #this condition check if the trackers is already connected and disconnect this tracker
        if (self.tracker_id == evt.GetSelection()) and (self.trk_init is not None) and (self.tracker_id != 0):
            dlg.TrackerAlreadyConnected()
            self.tracker_rem_id = self.tracker_id
            self.RemoveTracker()
            self.choice_tracker.SetSelection(0)
            self.SetTrackerFiducialsNone()
            self.tracker_id = 0
        else:
            self.tracker_id = evt.GetSelection()
            if self.tracker_id != 0:
                trck = {1 : dt.Tracker().ClaronTracker,
                        2 : dt.Tracker().PlhFastrak,
                        3 : dt.Tracker().PlhIsotrakII,
                        4 : dt.Tracker().PlhPatriot,
                        5 : dt.Tracker().ZebrisCMS20}
                self.tracker_rem_id = self.tracker_id
                self.trk_init = trck[self.tracker_id]()
                if self.trk_init is None:
                    self.RemoveTracker()
                    self.choice_tracker.SetSelection(0)
                    self.tracker_id = 0
                    self.tracker_rem_id = 0
                    self.SetTrackerFiducialsNone()
                else:
                    print "Tracker changed!"
            else:
                try:
                    self.RemoveTracker()
                    self.tracker_rem_id = 0
                except:
                    print "No tracker connected"
                self.SetTrackerFiducialsNone()
                print "Select Tracker"

    def RemoveTracker(self):
        remove_trck = {1: dt.RemoveTracker().ClaronTracker,
                2: dt.RemoveTracker().PlhFastrak,
                3: dt.RemoveTracker().PlhIsotrakII,
                4: dt.RemoveTracker().PlhPatriot,
                5: dt.RemoveTracker().ZebrisCMS20}
        rem = remove_trck[self.tracker_rem_id]()
        self.trk_init = None

    def OnChoiceRefMode(self, evt):
        self.ref_mode_id = evt.GetSelection()
        print "Ref_Mode changed!"
        #When ref mode is changed the tracker coords are set as null, self.aux_trck is the flag that sets it
        self.SetTrackerFiducialsNone()

    def SetTrackerFiducialsNone(self):
        self.numCtrl1d.SetValue(0)
        self.numCtrl2d.SetValue(0)
        self.numCtrl3d.SetValue(0)
        self.aux_trck1 = 0

        self.numCtrl1e.SetValue(0)
        self.numCtrl2e.SetValue(0)
        self.numCtrl3e.SetValue(0)
        self.aux_trck2 = 0

        self.numCtrl1f.SetValue(0)
        self.numCtrl2f.SetValue(0)
        self.numCtrl3f.SetValue(0)
        self.aux_trck3 = 0

    def Corregistration(self):
        self.M, self.q1, self.Minv = db.base_creation(self.coord1a,
                                                      self.coord2a,
                                                      self.coord3a)
        self.N, self.q2, self.Ninv = db.base_creation(self.coord1b,
                                                      self.coord2b,
                                                      self.coord3b)
        Publisher.sendMessage('Corregistrate Object', [self.Minv,
                                                       self.N,
                                                       self.q1,
                                                       self.q2,
                                                       self.trk_init,
                                                       self.tracker_id,
                                                       self.ref_mode_id,
                                                       self.a,
                                                       self.coord3a])