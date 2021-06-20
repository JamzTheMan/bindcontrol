import wx
import UI
from KeyBind.FileKeyBind import FileKeyBind

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

from Page import Page
from UI.ControlGroup import ControlGroup

import BindFile

class Mastermind(Page):
    petCommandKeyDefinitions = (
            {
                'label'      : 'Select All Pets',
                'ctrlName'      : 'PetSelectAll',
                'tooltipdetail' : 'select all of your pets',
            },
            {
                'label'      : 'Select Minions',
                'ctrlName'      : 'PetSelectMinions',
                'tooltipdetail' : 'select your "minion" pets',
            },
            {
                'label'      : 'Select Lieutenants',
                'ctrlName'      : 'PetSelectLieutenants',
                'tooltipdetail' : 'select your "lieutenant" pets',
            },
            {
                'label'      : 'Select Boss',
                'ctrlName'      : 'PetSelectBoss',
                'tooltipdetail' : 'select your "boss" pet',
            },
            {
                'label'      : 'Aggressive',
                'ctrlName'      : 'PetAggressive',
                'tooltipdetail' : 'set your selected pets to "Aggressive" mode',
            },
            {
                'label'      : 'Defensive',
                'ctrlName'      : 'PetDefensive',
                'tooltipdetail' : 'set your selected pets to "Defensive" mode',
            },
            {
                'label'      : 'Passive',
                'ctrlName'      : 'PetPassive',
                'tooltipdetail' : 'set your selected pets to "Passive" mode',
            },
            {
                'label'      : 'Attack',
                'ctrlName'      : 'PetAttack',
                'tooltipdetail' : 'order your selected pets to Attack your target',
            },
            {
                'label'      : 'Follow',
                'ctrlName'      : 'PetFollow',
                'tooltipdetail' : 'order your selected pets to Follow you',
            },
            {
                'label'      : 'Go To',
                'ctrlName'      : 'PetGoto',
                'tooltipdetail' : 'order your selected pets to Go To a targeted location',
            },
            {
                'label'      : 'Stay',
                'ctrlName'      : 'PetStay',
                'tooltipdetail' : 'order your selected pets to Stay at their current location',
            },
        )

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Profile = parent
        self.Init = {
            'Enable' : False,

            'PetSelectAll' : 'NUMPAD0',
            'PetSelectAllResponse' : 'Orders?',
            'PetSelectAllResponseMethod' : 'Local',

            'PetSelectMinions' : 'NUMPAD1',
            'PetSelectMinionsResponse' : 'Orders?',
            'PetSelectMinionsResponseMethod' : 'Self-tell',

            'PetSelectLieutenants' : 'NUMPAD2',
            'PetSelectLieutenantsResponse' : 'Orders?',
            'PetSelectLieutenantsResponseMethod' : '---',

            'PetSelectBoss' : 'NUMPAD3',
            'PetSelectBossResponse' : 'Orders?',
            'PetSelectBossResponseMethod' : 'Petsay',

            'PetBodyguard' : 'LSHIFT+NUMPAD5',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetAggressive' : 'NUMPAD4',
            'PetAggressiveResponse' : 'Kill On Sight.',
            'PetAggressiveResponseMethod' : 'Petsay',

            'PetDefensive' : 'NUMPAD5',
            'PetDefensiveResponse' : 'Return Fire Only.',
            'PetDefensiveResponseMethod' : 'Petsay',

            'PetPassive' : 'NUMPAD6',
            'PetPassiveResponse' : 'At Ease.',
            'PetPassiveResponseMethod' : 'Petsay',

            'PetAttack' : 'NUMPAD7',
            'PetAttackResponse' : 'Open Fire!',
            'PetAttackResponseMethod' : 'Petsay',

            'PetFollow' : 'NUMPAD8',
            'PetFollowResponse' : 'Falling In.',
            'PetFollowResponseMethod' : 'Petsay',

            'PetGoto' : 'NUMPAD9',
            'PetGotoResponse' : 'Moving To Checkpoint.',
            'PetGotoResponseMethod' : 'Petsay',

            'PetStay' : 'DECIMAL',
            'PetStayResponse' : 'Holding This Position.',
            'PetStayResponseMethod' : 'Petsay',

            'PetBodyguardEnabled' : 1,
            'PetBodyguardAttackEnabled' : True,
            'PetBodyguardGotoEnabled' : True,
            'PetBodyguardAttack' : 'LSHIFT+NUMPAD7',
            'PetBodyguardGoto' : 'LSHIFT+NUMPAD9',


            'EnablePetActionBinds': 1,

            'PetChatToggle' : 'LALT+M',
            'PetSelect1' : 'F1',
            'PetSelect2' : 'F2',
            'PetSelect3' : 'F3',
            'PetSelect4' : 'F4',
            'PetSelect5' : 'F5',
            'PetSelect6' : 'F6',

            'Pet1Name' : 'test1',
            'Pet2Name' : 'test2',
            'Pet3Name' : 'test3',
            'Pet4Name' : 'test4',
            'Pet5Name' : 'test5',
            'Pet6Name' : 'test6',

            'Pet1Bodyguard' : 0,
            'Pet2Bodyguard' : 1,
            'Pet3Bodyguard' : 0,
            'Pet4Bodyguard' : 0,
            'Pet5Bodyguard' : 1,
            'Pet6Bodyguard' : 0,
        }
        self.MMPowerSets = {
            "Beast Mastery"   : { 'min' : 'wol', 'lts'  : 'lio', 'bos'  : 'dir' },
            "Demon Summoning" : { 'min' : 'lin', 'lts'  : 'mons', 'bos' : 'pri' },
            "Mercenaries"     : { 'min' : "sol",  'lts' : "spec", 'bos' : "com", },
            "Necromancy"      : { 'min' : "zom",  'lts' : "grav", 'bos' : "lich", },
            "Ninjas"          : { 'min' : "gen",  'lts' : "joun", 'bos' : "oni", },
            "Robotics"        : { 'min' : "dron", 'lts' : "prot", 'bos' : "ass", },
            "Thugs"           : { 'min' : "thu",  'lts' : "enf",  'bos' : "bru", },
        }
        self.TabTitle = "Mastermind / Pet Binds"

    def BuildPage(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        petCommandsKeys = ControlGroup(self, self, width = 5, label = "Pet Action Binds", flexcols = [4])

        petCommandsKeys.AddControl( ctlName = 'spacer', ctlType = 'statictext', noLabel = True,)
        useCB = petCommandsKeys.AddControl(
            noLabel = True,
            ctlName = 'EnablePetActionBinds',
            ctlType = 'checkbox',
            contents = "Enable Pet Action Binds",
            tooltip = 'Check this to enable the Mastermind Pet Action Binds'
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetChatToggle',
            ctlType = 'keybutton',
            tooltip = 'Choose the key combo that will toggle your pet\'s Chatty Mode',
        )
        petCommandsKeys.AddControl( ctlName = 'spacer', ctlType = 'statictext', noLabel = True,)

        # Iterate the data structure at the top and make the grid of controls for the basic pet binds
        for command in self.petCommandKeyDefinitions:

            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'],
                ctlType = 'keybutton',
                tooltip = "Choose the key combo that will " + command['tooltipdetail'],
            )
            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'] + 'ResponseMethod',
                ctlType = 'combobox',
                contents = [ "Local", "Self-tell", "Petsay", "---", ],
                tooltip = "Choose how your pets will respond when they are in chatty mode and you " + command['tooltipdetail'],
            )
            petCommandsKeys.AddControl(
                noLabel = True,
                ctlName = command['ctrlName'] + "Response",
                ctlType = "text",
                tooltip = "Choose the chat response your pets give when you " + command['tooltipdetail'],
            )

        ### Bodyguard mode controls packed into the spacer differently
        petCommandsKeys.AddControl( ctlName = f'spacer1', ctlType = 'statictext', noLabel = True,)

        bgCB = petCommandsKeys.AddControl(
            noLabel  = True,
            ctlName  = 'PetBodyguardEnabled',
            ctlType  = 'checkbox',
            contents = 'Enable Bodyguard Mode Binds',
            tooltip  = 'Check this to enable the Bodyguard Mode Binds',
        )
        bgCB.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)

        # Add a blank row
        for i in [3,4,5]:
            petCommandsKeys.AddControl( ctlName = f'spacer{i}', ctlType = 'statictext', noLabel = True,)

        petCommandsKeys.AddControl(
            ctlType = 'keybutton',
            ctlName = 'PetBodyguard',
            tooltip = 'Choose the key combo that will put your designated pets into Bodyguard mode, while still commanding the others',
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardResponseMethod',
            ctlType = 'combobox',
            contents = [ "Local", "Self-tell", "Petsay", "---", ],
            tooltip = "Choose how your pets will respond when they are in chatty mode and you put your designated pets into Bodyguard mode, while still commanding the others",
        )
        petCommandsKeys.AddControl(
            noLabel = True,
            ctlName = "PetBodyguardResponse",
            ctlType = "text",
            tooltip = "Choose the chat response your pets give when you put your designated pets into Bodyguard mode, while still commanding the others",
        )
        # BGAttack and BGGoto formatted differently
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardAttack',
            ctlType = 'keybutton',
            tooltip = "Choose the key combo that will command your bodyguards to attack your target",
        )
        staticbox = petCommandsKeys.GetStaticBox()
        enableBGAttack = wx.CheckBox(staticbox, -1, "Enable")
        enableBGAttack.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)
        enableBGAttack.SetValue(bool(self.Init['PetBodyguardAttackEnabled']))
        self.Ctrls['PetBodyguardAttackEnabled'] = enableBGAttack
        petCommandsKeys.InnerSizer.Add(enableBGAttack, 0, wx.ALL|wx.EXPAND, 5)
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))

        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardGoto',
            ctlType = 'keybutton',
            tooltip = "Choose the key combo that will command your bodyguards to go to a targeted location",
        )
        enableBGGoto = wx.CheckBox(petCommandsKeys.GetStaticBox(), -1, "Enable")
        enableBGGoto.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)
        enableBGGoto.SetValue(bool(self.Init['PetBodyguardGotoEnabled']))
        self.Ctrls['PetBodyguardGotoEnabled'] = enableBGGoto
        petCommandsKeys.InnerSizer.Add(enableBGGoto, 0, wx.ALL|wx.EXPAND, 5)
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))

        # get the pet names, whether they're bodyguards, and binds to select them directly
        # TODO -- probably want to enable/disable various bits of this based on whether bodyguard is
        # active, or whether we have names, or whatever
        petNames = ControlGroup(self, self, width = 5, label = "Pet Names and By-Name Selection Binds",flexcols=[1,4])

        for PetID in range(1,7):

            petNames.AddControl(
                ctlName = f"Pet{PetID}Name",
                ctlType = 'text',
                tooltip = f"Specify Pet {PetID}'s Name for individual selection",
            )
            petNames.AddControl(
                noLabel = True,
                ctlName = f"Pet{PetID}Bodyguard",
                ctlType = 'checkbox',
                contents = "Bodyguard",
                tooltip = f"Select whether pet {PetID} acts as Bodyguard",
            )
            petNames.AddControl(
                ctlName = f"PetSelect{PetID}",
                ctlType = "keybutton",
                tooltip = f"Choose the Key Combo to Select Pet {PetID} by Name"
            )

        sizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 16)
        sizer.AddSpacer(10)
        sizer.Add(petNames, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 16)

        self.SetSizerAndFit(sizer)

        self.OnArchetypePowerChange()

    # not actually an event listener, gets called explicitly
    def OnArchetypePowerChange(self):
        arch = self.Profile.General.GetState('Archetype')
        pset = self.Profile.General.GetState('Primary')

        for _, control in self.Ctrls.items():
            control.Enable(bool(arch == "Mastermind" and pset))

    def OnBGCheckboxes(self, evt):
        bgEnabled = self.Ctrls['PetBodyguardEnabled']       .IsChecked()
        bgAttack  = self.Ctrls['PetBodyguardAttackEnabled'] .IsChecked()
        bgGoto    = self.Ctrls['PetBodyguardGotoEnabled']   .IsChecked()

        for c in ['PetBodyguard','PetBodyguardResponseMethod','PetBodyguardResponse']:
            self.Ctrls[c].Enable(bgEnabled)

        self.Ctrls['PetBodyguardAttack'].Enable(bgEnabled and bgAttack)
        self.Ctrls['PetBodyguardGoto']  .Enable(bgEnabled and bgGoto)

    def HelpText(self):
        return """
        The Original Mastermind Control Binds
        were created in CoV Beta by Khaiba
        a.k.a. Sandolphan
        Bodyguard code inspired directly from
        Sandolphan's Bodyguard binds.
        Thugs added by Konoko!
        """

    ### BIND CREATION METHODS
    def mmBGSelBind(self, profile, file, PetBodyguardResponse, powers):
        bgset = bgsay = []
        if (self.GetState('PetBodyguardEnabled')):
            (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.

            # emerson TODO -- this ~= '---' was in the original code but produces different results
            if (((tier1bg + tier2bg + tier3bg) == 6)):
                bgsay = [self.GetChatMethod('PetBodyguardResponseMethod') + PetBodyguardResponse]
            else:
                if (tier1bg == 3):
                    bgsay.append(f"petsaypow {powers['min']} {PetBodyguardResponse}")
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet1Name')} {PetBodyguardResponse}")
                    if (self.GetState('Pet2Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet2Name')} {PetBodyguardResponse}")
                    if (self.GetState('Pet3Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet3Name')} {PetBodyguardResponse}")

                if (tier2bg == 2):
                    bgsay.append(f"petsaypow {powers['lts']} {PetBodyguardResponse}")
                else:
                    if (self.GetState('Pet4Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet4Name')} {PetBodyguardResponse}")
                    if (self.GetState('Pet5Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet5Name')} {PetBodyguardResponse}")

                if (tier3bg == 1):
                    bgsay.append(f"petsaypow {powers['bos']} {PetBodyguardResponse}")

            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = ['petcomall def fol']
            else:
                if (tier1bg == 3):
                    bgset.append(f"petcompow {powers['min']} def fol")
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet1Name')} def fol")
                    if (self.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet2Name')} def fol")
                    if (self.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet3Name')} def fol")

                if (tier2bg == 2):
                    bgset.append(f"petcompow {powers['lts']} def fol")
                else:
                    if (self.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet4Name')} def fol")
                    if (self.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet5Name')} def fol")

                if (tier3bg == 1):
                    bgset.append(f"petcompow {powers['bos']} def fol")

            keyBindContents = bgsay + bgset + [profile.GetBindFile('mmbinds','cbguarda.txt').BLF()]
            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(keyBindContents))

    def mmBGActBind(self, profile, filedn, fileup, action, say, powers):

        key    = self.GetState(f"Pet{action}")
        method = self.GetChatMethod(f"Pet{action}ResponseMethod")

        bgact = bgsay = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 0)):
            bgsay = [method + say]
        else:
            if (tier1bg == 0):
                bgsay.append(f"petsaypow {powers['min']} $say")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet1Name')} {say}")
                if (not self.GetState('Pet2Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet2Name')} {say}")
                if (not self.GetState('Pet3Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet3Name')} {say}")

            if (tier2bg == 0):
                bgsay.append(f"petsaypow {powers['lts']} {say}")
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet4Name')} {say}")
                if (not self.GetState('Pet5Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet5Name')} {say}")

            if (tier3bg == 0):
                bgsay.append(f"petsaypow {powers['bos']} {say}")

        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = ['petcomall ' + action]
        else :
            if (tier1bg == 0):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (not self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (not self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (not self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 0):
                bgact.append('petcompow ' + f"{powers['bos']} {action}")

        filedn.SetBind(FileKeyBind(key = key, contents = bgsay + [fileup.BLF()]))
        fileup.SetBind(FileKeyBind(key = key, contents = bgact + [filedn.BLF()]))

    def mmBGActBGBind(self, profile, filedn, fileup, action, say, powers):
        key =    self.GetState(f"PetBodyguard{action}")
        method = self.GetChatMethod(f"Pet{action}ResponseMethod")

        bgact = bgsay = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 6)):
            bgsay = [method + say]
        else :
            if (tier1bg == 3):
                bgsay.append(f"petsaypow {powers['min']} {say}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet1Name')} {say}")
                if (self.GetState('Pet2Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet2Name')} {say}")
                if (self.GetState('Pet3Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet3Name')} {say}")

            if (tier2bg == 2):
                bgsay.append(f"petsaypow {powers['lts']} {say}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet4Name')} {say}")
                if (self.GetState('Pet5Bodyguard')) : bgsay.append(f"petsayname {self.GetState('Pet5Name')} {say}")

            if (tier3bg == 1):
                bgsay.append(f"petsaypow {powers['bos']} {say}")

        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = ['petcomall ' + action]
        else :
            if (tier1bg == 3):
                bgact.append(bgact + f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 1):
                bgact.append(f"petcompow {powers['bos']} {action}")

        # file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay.$bgset.BindFile.BLF($profile, 'mmbinds','\mmbinds\\cbguarda.txt')))
        filedn.SetBind(FileKeyBind(key = key, contents = bgsay + [fileup.BLF()]))
        fileup.SetBind(FileKeyBind(key = key, contents = bgact + [filedn.BLF()]))

    def mmQuietBGSelBind(self, profile, file, powers):
        if (self.GetState('PetBodyguardEnabled')):
            bgset = []
            (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = ["petcomall def fol"]
            else :
                if (tier1bg == 3):
                    bgset.append(f"petcompow {powers['min']} def fol")
                else :
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet1Name')} def fol")
                    if (self.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet2Name')} def fol")
                    if (self.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet3Name')} def fol")

                if (tier2bg == 2):
                    bgset.append(f"petcompow {powers['lts']} def fol")
                else :
                    if (self.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet4Name')} def fol")
                    if (self.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet5Name')} def fol")

                if (tier3bg == 1):
                    bgset.append(f"petcompow {powers['bos']} def fol")

            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgset + [profile.GetBindFile('mmbinds','bguarda.txt').BLF()]))

    def mmQuietBGActBind(self, profile, filedn, fileup, action, powers):

        key = self.GetState(f"Pet{action}")

        bgact = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = [f"petcomall {action}"]
        else :
            if (tier1bg == 0):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (not self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (not self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (not self.GetState('Pet5Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 0): bgact.append(f"petcompow {powers['bos']} {action}")

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(FileKeyBind(key = key, contents = bgact))

    def mmQuietBGActBGBind(self, profile, filedn, fileup, action, powers):

        key    = self.GetState(f"PetBodyguard{action}")

        bgact = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = [f"petcomall {action}"]
        else :
            if (tier1bg == 3):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow  {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 1) : bgact.append(f"petcompow {powers['bos']} {action}")

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(FileKeyBind(key = key, contents = bgact))

    def mmSubBind(self, profile, file, fn, grp, powers):
        PetResponses = {}
        for cmd in ('SelectAll', 'SelectMinions', 'SelectLieutenants', 'SelectBoss', 
                'Aggressive', 'Defensive', 'Passive', 'Attack', 'Follow', 'Goto', 'Stay','Bodyguard',):
            PetResponses[cmd] = ''
            if self.GetChatMethod(f"Pet{cmd}ResponseMethod") : PetResponses[cmd] = self.GetState(f"Pet{cmd}Response")

        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectAllResponseMethod') + f"{PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectMinionsResponseMethod', 'min') + f"{PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectLieutenantsResponseMethod', 'lts') + f"{PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectBossResponseMethod', 'bos') + f"{PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))

        self.mmBGSelBind(profile,file,PetResponses['Bodyguard'],powers)

        if grp: petcom = f"$$petcompow {grp}"
        else:   petcom =  "$$petcomall"
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(self.GetChatMethod(f"Pet{cmd}ResponseMethod") + f"{PetResponses[cmd]}{petcom} {cmd}"))

        if (self.GetState('PetBodyguardAttackEnabled'))  : file.SetBind(self.Ctrls['PetBodyguardAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBodyguardGotoEnabled'))    : file.SetBind(self.Ctrls['PetBodyguardGoto'].MakeFileKeyBind('nop'))
        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}.txt").BLF()]))

    def mmBGSubBind(self, profile, filedn, fileup, fn, powers):
        PetResponses = {}
        for cmd in ('SelectAll','SelectMinions','SelectLieutenants','SelectBoss','Aggressive','Defensive','Passive','Attack','Follow','Goto', 'Stay', 'Bodyguard',):
            PetResponses[cmd] = ''
            if self.GetChatMethod(f'Pet{cmd}ResponseMethod') : PetResponses[cmd] = self.GetState(f'Pet{cmd}Response')

        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectAllResponseMethod') + f"{PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectMinionsResponseMethod', 'min') + f"{PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectLieutenantsResponseMethod', 'lts') + f"{PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectBossResponseMethod', 'bos') + f"{PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))
        self.mmBGSelBind(profile,filedn,PetResponses['Bodyguard'],powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            self.mmBGActBind(profile, filedn, fileup, cmd, PetResponses[cmd], powers)

        if (self.GetState('PetBodyguardAttackEnabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Attack', PetResponses['Attack'], powers)

        if (self.GetState('PetBodyguardGotoEnabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Goto', PetResponses['Goto'], powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}a.txt").BLF()]))

    def mmQuietSubBind(self, profile, file, fn, grp, powers):
        file.SetBind(self.Ctrls['PetSelectAll']        .MakeFileKeyBind(profile.GetBindFile('mmbinds','  all.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectMinions']    .MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectBoss']       .MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))
        self.mmQuietBGSelBind(profile, file, powers)

        if grp: petcom = f"petcompow {grp}"
        else:   petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        if (self.GetState('PetBodyguardAttackEnabled'))  : file.SetBind(self.Ctrls['PetBodyguardAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBodyguardGotoEnabled'))    : file.SetBind(self.Ctrls['PetBodyguardGoto'].MakeFileKeyBind('nop'))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmbinds','c' + fn + '.txt').BLF()]))

    def mmQuietBGSubBind(self, profile, filedn, fileup, fn, powers):
        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(profile.GetBindFile('mmbinds','all.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))

        self.mmQuietBGSelBind(profile,filedn,powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack', 'Follow','Stay', 'Goto'):
            self.mmQuietBGActBind(profile, filedn, fileup, cmd, powers)

        if (self.GetState('PetBodyguardAttackEnabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Attack', powers)

        if (self.GetState('PetBodyguardGotoEnabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Goto', powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmbinds','c' + fn + 'a.txt').BLF()]))

    def PopulateBindFiles(self):

        ### TODO
        #return
        ### TODO

        profile = self.Profile

        ResetFile = profile.ResetFile()

        if (self.GetState('PetSelEnable')):
            if (self.GetState('Pet1Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel0'].MakeFileKeyBind(f"petselectname {self.GetState('Pet1Name')}"))
            if (self.GetState('Pet2Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel1'].MakeFileKeyBind(f"petselectname {self.GetState('Pet2Name')}"))
            if (self.GetState('Pet3Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel2'].MakeFileKeyBind(f"petselectname {self.GetState('Pet3Name')}"))
            if (self.GetState('Pet4Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel3'].MakeFileKeyBind(f"petselectname {self.GetState('Pet4Name')}"))
            if (self.GetState('Pet5Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel4'].MakeFileKeyBind(f"petselectname {self.GetState('Pet5Name')}"))
            if (self.GetState('Pet6Nameenabled')) :
                ResetFile.SetBind(self.Ctrls['sel5'].MakeFileKeyBind(f"petselectname {self.GetState('Pet6Name')}"))

        powers = self.MMPowerSets[ profile.General.GetState('Primary') ]

        #### "Quiet" versions
        allfile = profile.GetBindFile('mmbinds','all.txt')
        minfile = profile.GetBindFile('mmbinds','tier1.txt')
        ltsfile = profile.GetBindFile('mmbinds','tier2.txt')
        bosfile = profile.GetBindFile('mmbinds','tier3.txt')

        if (self.GetState('PetBodyguardEnabled')):
            bgfiledn = profile.GetBindFile('mmbinds','bguarda.txt')
            bgfileup = profile.GetBindFile('mmbinds','bguardb.txt')
        self.mmSubBind(profile      , ResetFile   , "all"    , None          , powers)
        self.mmQuietSubBind(profile , allfile     , "all"    , None          , powers)
        self.mmQuietSubBind(profile , minfile     , "tier1"  , powers['min'] , powers)
        self.mmQuietSubBind(profile , ltsfile     , "tier2"  , powers['lts'] , powers)
        self.mmQuietSubBind(profile , bosfile     , "tier3"  , powers['bos'] , powers)
        if (self.GetState('PetBodyguardEnabled')):
            self.mmQuietBGSubBind(profile,bgfiledn,bgfileup,"bguard",powers)

        #### "Chatty" versions
        callfile = profile.GetBindFile('mmbinds','call.txt')
        cminfile = profile.GetBindFile('mmbinds','ctier1.txt')
        cltsfile = profile.GetBindFile('mmbinds','ctier2.txt')
        cbosfile = profile.GetBindFile('mmbinds','ctier3.txt')

        if (self.GetState('PetBodyguardEnabled')):
            cbgfiledn = profile.GetBindFile('mmbinds','cbguarda.txt')
            cbgfileup = profile.GetBindFile('mmbinds','cbguardb.txt')
        self.mmSubBind(profile , callfile , "all"   , None          , powers)
        self.mmSubBind(profile , cminfile , "tier1" , powers['min'] , powers)
        self.mmSubBind(profile , cltsfile , "tier2" , powers['lts'] , powers)
        self.mmSubBind(profile , cbosfile , "tier3" , powers['bos'] , powers)
        if (self.GetState('PetBodyguardEnabled')):
            self.mmBGSubBind(profile,cbgfiledn,cbgfileup,"bguard",powers)

    def GetChatMethod(self, control, target = 'all'):
        chatdesc = self.GetState(control)
        powers   = self.MMPowerSets[ self.Profile.General.GetState('Primary') ]
        # This is terrible, I accidentally optimized away the original way of doing this.
        if target == "all": petsay = "petsayall "
        else:               petsay = "petsaypow " + powers[target] + " "

        return {
            'Local'     : 'local ',
            'Self-tell' : 'tell $name, ',
            'Petsay'    : petsay,
            '---'       : '',
        }[chatdesc]

    def CountBodyguards(self):
        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
        #  so, add all fullgroups into the bgsay command.
        tier1bg = tier2bg = tier3bg = 0
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        return (tier1bg, tier2bg, tier3bg)


    for cmd in petCommandKeyDefinitions:
        UI.Labels[cmd['ctrlName']] = cmd['label']
    UI.Labels.update({
        'PetSelEnable'                       : "Enable By-Name Pet Selection",
        'Pet1Name'                           : "First Pet's Name",
        'Pet2Name'                           : "Second Pet's Name",
        'Pet3Name'                           : "Third Pet's Name",
        'Pet4Name'                           : "Fourth Pet's Name",
        'Pet5Name'                           : "Fifth Pet's Name",
        'Pet6Name'                           : "Sixth Pet's Name",
        'PetSelect1'                         : "Select First Pet",
        'PetSelect2'                         : "Select Second Pet",
        'PetSelect3'                         : "Select Third Pet",
        'PetSelect4'                         : "Select Fourth Pet",
        'PetSelect5'                         : "Select Fifth Pet",
        'PetSelect6'                         : "Select Sixth Pet",
        'PetSelectAllResponseMethod'         : "Response to Select All Pets",
        'PetSelectMinionsResponseMethod'     : "Response to Select Minions",
        'PetSelectLieutenantsResponseMethod' : "Response to Select Lieutenants",
        'PetSelectBossResponseMethod'        : "Response to Select Boss",
        'PetAggressiveResponseMethod'        : "Response to Set Aggressive",
        'PetDefensiveResponseMethod'         : "Response to Set Defensive",
        'PetPassiveResponseMethod'           : "Response to Set Passive",
        'PetAttackResponseMethod'            : "Response to Attack",
        'PetFollowResponseMethod'            : "Response to Follow",
        'PetGotoResponseMethod'              : "Response to Goto",
        'PetStayResponseMethod'              : "Response to Stay",
        'PetBodyguard'                       : "Bodyguard Mode",
        'PetBodyguardResponseMethod'         : "Response to Bodyguard Mode",
        'PetChatToggle'                      : "Chat Mode Toggle",
        'PetBodyguardAttack'                 : "BG Mode Attack",
        'PetBodyguardGoto'                   : "BG Mode Goto",
    })
