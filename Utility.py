import wx
import re
import UI

conflictbinds = {
    'binds' : {},
    'conflicts' : {},
}

def ColorDefault():
    return {
        'border'     : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'foreground' : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'background' : { 'r' : 255, 'g' : 255, 'b' : 255, },
    }

def BLF(profile, *args):
    return "bindloadfile " + BLFPath(profile, *args)

def BLFPath(profile, *args):
    # TODO TODO TODO -- os-agnostic please
    filepath = profile.BindsDir()
    for arg in args:
        filepath = filepath + "/" + arg

    return filepath

Icons = {}
def Icon(iconname):
    if not Icons.get('iconname', None):
        # TODO - platform-agnostic file paths
        Icons[iconname] = wx.Bitmap(
            wx.Image(
                f"icons/{iconname}.png", wx.BITMAP_TYPE_ANY, -1,
            )
        )
    return Icons[iconname]

#####
# disable controls by name
def DisableControls(page, enabled, names):
    for name in names:
        page.Ctrls[name].Enable(enabled)
        page.Ctrls[name].ctlLabel.Enable(enabled)


#####################################################
from UI.ControlGroup import bcKeyButton
def CheckConflict(profile, key):
    conflicts = []

    for pageName in profile.Pages:
        page = getattr(profile, pageName, None)
        for ctrlname, ctrl in page.Ctrls.items():
            if not ctrl.IsEnabled(): continue
            if isinstance(ctrl, bcKeyButton):
                if key == ctrl.GetLabel():
                    print(f"conflict found for key {key}: page {pageName}, {UI.Labels[ctrlname]}")
                    conflicts.append( {'page' : pageName, 'ctrl': UI.Labels[ctrlname]})
    return conflicts


def getMainKey(key):
    return re.sub('[LR]?(SHIFT|CTRL|ALT)\+?', '', key)

def ChatColors(fg,bg,bd): return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

__DATA__ = """

local cats = {}
local mods = {}
local profile = {}
profile.__index = profile
dialogs = {}
dlgs_mt = {__mode="k"}
setmetatable(dialogs,dlgs_mt)
local filelist = {}

local fmt = {__index={close=function() end}}

local progressbar
local progressdialog
local numbinds = 0
local progress = 0
local pbmax = 0
local conflictbinds

function cbWriteFile(f)
    local file = assert(io.open(f.filename,f.mode))
    --add in bind sorter here
    table.sort(f.binds,function(a,b)
        return getMainKey(a.key) < getMainKey(b.key)
    end)
    local i = 0
    for _,v in ipairs(f.binds) do
        incProgBar()
        file:write(v.s)
        i = i + 1
    end
    file:close()
    return i
end

function cbResolveConflict(conflict,key,profile)
    local clist = {}
    local conflictdlg
    table.insert(clist,iup.label{title = "\n  Please Resolve these Keybind Conflicts and close this window when you are done.\n\n"})
    for i,v in ipairs(conflict) do
        table.insert(clist,(cbBindBox(v.purpose,v.t,v.k,nil,profile,nil,nil,300,nil,function() conflictdlg.bringfront="YES" end)))
    end
    conflictdlg = iup.dialog{iup.vbox(clist),maxbox="NO",resize="NO",title="Conflict Resolution"}
    iup.Popup(conflictdlg,iup.CENTER,iup.CENTER)
end

local resetstring

function cbGetBaseReset(profile)
    --return ""
    return "$$bind_load_file "..profile.base.."\\subreset.txt"
end

function cbAddReset(s)
    resetstring = resetstring.."$$"..s
end

function cbResolveKeyConflicts(self,initprogbar)
    if initprogbar then
        local modcount = 0
        for _,module in pairs(mods) do
            if module.bindisused(self) then
                modcount = modcount+1
            end
        end
        newProgBar("Generating Bindfiles",modcount)
    end
    conflictbinds = {}
    conflictbinds.binds = {}
    conflictbinds['conflicts'] = {}
    setProgBarText("Finding Conflicts")
    for _,module in pairs(mods) do
        if module.bindisused(self) then
            incProgBar()
            module.findconflicts(self)
        end
    end
    cbCheckConflict(self,"ResetKey","Binds Reset Key")
    local conflicts = {}
    for k,v in pairs(conflictbinds['conflicts']) do table.insert(conflicts,{v=v,k=k}) table.sort(conflicts,function(a,b) return a.v[1].keybase < b.v[1].keybase end) end
    resetProgBar(table.getn(conflicts),"Resolving Conflicts")
    for i,v in ipairs(conflicts) do
        incProgBar()
        cbResolveConflict(v.v,v.k,self)
    end
    conflictbinds = nil
    if initprogbar then
        delProgBar()
    end
end

local resetfile1
local resetfile2
local resetkey

local activeprofile

function profile:write()
    -- adding a check here to indicate that spaces in profile paths are not likely to be usable.
    activeprofile = self
    if (string.find(self.base," ",1,true)) then
        iup.Message("WARNING!","Using a Bind Directory with spaces will NOT work when you try to /bindloadfile, remove the spaces!")
        return
    end
    local ret,err = cbMakeDirectory(self.base)
    if not cbFileExists(self.base) then iup.Message("",self.base.." "..err) end
    self.resetfile = cbOpen(self.base .. "\\reset.txt","w")
    resetfile1 = self.resetfile
    resetkey = self.ResetKey
    resetfile2 = cbOpen(self.base .. "\\subreset.txt","w")
    resetstring = "bind_load_file "..self.base.."\\reset.txt"
    if self.resetnotice then
        resetstring = resetstring.."$$tell $name, Keybinds reloaded."
    end
    if self.resetfile == nil then iup.Message("Error", "Resetfile not created!") end
    local modcount = 0
    for _,module in pairs(mods) do
        if module.bindisused(self) then
            modcount = modcount+1
        end
    end
    newProgBar("Generating Bindfiles",modcount)
    cbResolveKeyConflicts(self)
    resetProgBar(modcount," ")
    for _,module in pairs(mods) do
        if module.bindisused(self) then
            setProgBarText(module.label)
            incProgBar()
            module.makebind(self)
        end
    end
    cbWriteBind(self.resetfile,self.ResetKey,resetstring)
    self.resetfile:close()
    resetfile2:close()
    resetProgBar(numbinds,"Writing Files")
    local count = 0
    for k,v in pairs(filelist) do
        count = count + cbWriteFile(v)
    end
    delProgBar()
    self.resetfile = nil
    resetfile1 = nil
    resetfile2 = nil
    resetkey = nil
    --iup.Message("Saved "..count.." binds","Done!\n\nNow log on to the character you made this for and type:\n\n/bindloadfile "..self.base.."\\reset.txt\n\nMake sure you use the \\ Backslash key for the file location!")
    local top = iup.vbox{iup.fill{rastersize="10x10"},iup.label{title="Done!\n\nNow log on to the character you made this for and type:\n",expand="YES",alignment="ACENTER"},iup.fill{rastersize="10x10"}}
    local textitem = iup.text{value="/bindloadfile "..self.base.."\\reset.txt",readonly="YES",expand="YES",alignment="ACENTER"}
    local bottom = iup.vbox{iup.fill{rastersize="10x10"},iup.label{title="If you are reloading binds on your character, \nyou may also be able to just hit your Reset Key and reset your binds.",alignment="ACENTER"},iup.fill{rastersize="10x10"}}
    local finished = iup.dialog{iup.hbox{iup.fill{rastersize="10x"},iup.vbox{top,textitem,bottom},iup.fill{rastersize="10x"}},title="Saved "..count.." binds",maxbox="NO",minbox="NO",resize="NO"}
    finished:popup(iup.CENTER,iup.CENTER)
    cbdlg.bringfront="YES"
    activeprofile = nil
end

function cbNewBind(str)
    str = str or "UNBOUND"
    str = string.upper(str)
    local mkey,shift,ctrl,alt
    if string.find(str,"LSHIFT") then shift = "LSHIFT" end
    str = string.gsub(str,"LSHIFT","")
    if string.find(str,"RSHIFT") then shift = "RSHIFT" end
    str = string.gsub(str,"RSHIFT","")
    if string.find(str,"SHIFT") then shift = "LSHIFT" end
    str = string.gsub(str,"SHIFT","")
    if string.find(str,"LCTRL") then ctrl = "LCTRL" end
    str = string.gsub(str,"LCTRL","")
    if string.find(str,"RCTRL") then ctrl = "RCTRL" end
    str = string.gsub(str,"RCTRL","")
    if string.find(str,"CTRL") then ctrl = "LCTRL" end
    str = string.gsub(str,"CTRL","")
    if string.find(str,"LALT") then alt = "LALT" end
    str = string.gsub(str,"LALT","")
    if string.find(str,"RALT") then alt = "RALT" end
    str = string.gsub(str,"RALT","")
    if string.find(str,"ALT") then alt = "LCTRL" end
    str = string.gsub(str,"ALT","")
    mkey = string.gsub(str,"%+","")
    local t={}
    t.mainkey = mkey
    t.shift = shift
    t.ctrl = ctrl
    t.alt = alt
    t.bind = t.shift
    if (not t.bind) and t.ctrl then
        t.bind = t.ctrl
    elseif t.bind and t.ctrl then
        t.bind = t.bind.."+"..t.ctrl
    end
    if (not t.bind) and t.alt then
        t.bind = t.alt
    elseif t.bind and t.alt then
        t.bind = t.bind.."+"..t.alt
    end
    if (not t.bind) and t.mainkey then
        t.bind = t.mainkey
    elseif t.bind and not (t.mainkey == "") then
        t.bind = t.bind.."+"..t.mainkey
    end
    if not t.bind then t.bind = "" end
    return t
end

function cbSetBind(bindkey,curbind)
    bindkey = string.upper(bindkey)
    bindkey = string.upper(bindkey)
    if bindkey=="LSHIFT" or bindkey=="RSHIFT" then
        if bindkey==curbind.shift then
            curbind.shift=nil
        else
            curbind.shift = bindkey
        end
    elseif bindkey=="LCTRL" or bindkey=="RCTRL" then
        if bindkey==curbind.ctrl then
            curbind.ctrl=nil
        else
            curbind.ctrl = bindkey
        end
    elseif bindkey=="LALT" or bindkey=="RALT" then
        if bindkey==curbind.alt then
            curbind.alt=nil
        else
            curbind.alt = bindkey
        end
    else
        if curbind.mainkey == bindkey then
            curbind.mainkey = ""
        else
            curbind.mainkey = bindkey
        end
    end
    curbind.bind = curbind.shift
    if (not curbind.bind) and curbind.ctrl then
        curbind.bind = curbind.ctrl
    elseif curbind.bind and curbind.ctrl then
        curbind.bind = curbind.bind.."+"..curbind.ctrl
    end
    if (not curbind.bind) and curbind.alt then
        curbind.bind = curbind.alt
    elseif curbind.bind and curbind.alt then
        curbind.bind = curbind.bind.."+"..curbind.alt
    end
    if (not curbind.bind) and curbind.mainkey then
        curbind.bind = curbind.mainkey
    elseif curbind.bind and curbind.mainkey then
        curbind.bind = curbind.bind.."+"..curbind.mainkey
    end
    if not curbind.bind then curbind.bind = "" end
    curbind.bind = string.gsub(curbind.bind,"%+$","")
    if curbind.bind == "" then curbind.bind = "UNBOUND" end
end

function cbSetDesc(profile,bindkey,desc,label,t,k)
    if not bindkey then return end
    profile.binds = profile.binds or {}
    profile.binds_label = profile.binds_label or {}
    profile.binds_tk = profile.binds_tk or {}
    if type(desc) == "function" then
        profile.binds[bindkey] = desc()
    else
        profile.binds[bindkey] = desc
    end
    profile.binds_label[bindkey] = label
    profile.binds_tk[bindkey] = {t = t; k = k}
end

function cbMakeDescLink(prefix,t,k,suffix)
    local o = {}
    o.prefix = prefix or ""
    o.t = t
    o.k = k
    o.suffix = suffix or ""
    return o
end

function cbGetDesc(profile,bindkey)
    if profile.binds then
        if type(profile.binds[bindkey]) == "table" then
            if not profile.binds[bindkey].t[profile.binds[bindkey].k] then return profile.binds[bindkey].prefix.."Unknown"..profile.binds[bindkey].suffix end
            return profile.binds[bindkey].prefix..profile.binds[bindkey].t[profile.binds[bindkey].k]..profile.binds[bindkey].suffix
        else
            return profile.binds[bindkey] or "Unbound"
        end
    else
        return "Unknown"
    end
end

function cbUnboundOrEqualTo(a,b,profile)
    profile.binds = profile.binds or {}
    if profile.binds[a] then
        if string.upper(a) == "UNBOUND" then return true end
        return a == b
    else
        return true
    end
end

function cbGetBindKey(bkey,desc,profile,label,t,k)
    local curbind = cbNewBind(bkey)
    curbind = cbPopVKeyboard(curbind,profile) -- This shouldn't return until after a bindkey was chosen.
    if curbind then
        -- check to see if the new key is unbound or identical to bkey, if not, ask for confirmation
        if not cbUnboundOrEqualTo(curbind.bind,bkey,profile) then
            -- ask for confirm, if yes then
            if iup.Alarm("Overwrite "..cbGetDesc(profile,curbind.bind).."?","This key combo is used for a different bind.  Overwrite it?","No","Yes") == 2 then
                -- overwrite the original bind to no key, or UNBOUND
                profile.binds_tk[curbind.bind].t[profile.binds_tk[curbind.bind].k] = "UNBOUND"
                if profile.binds_label[curbind.bind] then
                    profile.binds_label[curbind.bind].title = "UNBOUND"
                end
                -- if the original key has a visible label indicating its status, reset its title.
                cbSetDesc(profile,bkey,nil,nil,nil,nil)
                cbSetDesc(profile,curbind.bind,desc,label,t,k)
                return curbind.bind
            else
                return bkey
            end
        else
            cbSetDesc(profile,bkey,nil,nil,nil,nil)
            cbSetDesc(profile,curbind.bind,desc,label,t,k)
            return curbind.bind
        end
    else
        return bkey
    end
end

function cbCheckBind(label,t,k,tgl,desc,profile,w,h,w2,h2,tglcb)
    local tk = t[k] or "UNBOUND"
    local val = string.upper(tk)
    local ttgl = "ON"
    if not t[tgl] then ttgl = "OFF" end
    w = w or 100
    h = h or 21
    w2 = w2 or 100
    h2 = h2 or 21
    desc = desc or label
    local ttext = iup.label{title = val; rastersize = (w-20).."x"}

    local tbtn = iup.button{title="..."; rastersize = "20x"..h, tip = cbTTip}
    tbtn.action = function()
        ttext.title = cbGetBindKey(t[k],desc,profile,ttext,t,k)
        profile.modified = true
        t[k] = ttext.title
    end
    if not t[tgl] then
        tbtn.active = "NO"
        ttext.active = "NO"
    end
    cbTTip = nil
    local lbl = iup.toggle{title = label; value=ttgl; rastersize = w2.."x"}
    lbl.action = function(_,v)
        profile.modified = true
        if v == 1 then
            t[tgl] = true
            tbtn.active = "YES"
            ttext.active = "YES"
        else
            t[tgl] = nil
            tbtn.active = "NO"
            ttext.active = "NO"
        end
        if tglcb then tglcb() end
    end
    return iup.hbox{lbl,ttext,tbtn;alignment="ACENTER"}
end

function cbListBox(label,list,numitems,val,callback,w,h,w2,h2,editable)
    w = w or 100
    h = h or 21
    w2 = w2 or 100
    h2 = h2 or 21
    local ttable = {}
    for i = 1,table.getn(list) do ttable[i] = list[i] end
    ttable.dropdown = "YES"
    ttable.visible_items = numitems
    ttable.value = val
    ttable.rastersize = w.."x"..h
    ttable.tip = cbTTip
    if editable then
        ttable.editbox = "YES"
    end
    if numitems > 20 then
        ttable.visible_items = 20
    end
    local tlist = iup.list(ttable)
    tlist.action = callback
    if editable then
        tlist.edit_cb = function(_,c,s) callback(_,s,nil,1) return iup.DEFAULT end
    end
    cbTTip = nil
    return iup.hbox{iup.label{title = label; rastersize = w2.."x"},tlist;alignment="ACENTER"},tlist
end

function cbPowerList(label,powerlist,t,v,profile,w,h,w2,h2)
    return cbListBox(label,powerlist,table.getn(powerlist),t[v],
        function(_,s,i,w)
            if w == 1 then t[v] = s end
            profile.modified = true
        end,
    w,h,w2,h2,true)
end

function cbTogglePower(label,powerlist,togval,t,v,togcb,profile,w,h,w2,h2)
    w = w or 100
    h = h or 21
    w2 = w2 or 100
    h2 = h2 or 21
    local ttable = {}
    for i = 1,table.getn(powerlist) do ttable[i] = powerlist[i] end
    ttable.dropdown = "YES"
    ttable.visible_items = numitems
    ttable.value = t[v]
    ttable.rastersize = w2.."x"..h2
    ttable.tip = cbTTip
    ttable.editbox = "YES"
    if table.getn(powerlist) > 20 then
        ttable.visible_items = 20
    end
    local tlist = iup.list(ttable)
    tlist.action = function(_,s,i,w)
        if w == 1 then t[v] = s end
        profile.modified = true
    end
    tlist.edit_cb = function(_,c,s) tlist.action(_,s,nil,1) end

    if not togval then tlist.active = "NO" end

    local chkval
    if togval then chkval = "ON" else chkval = "OFF" end

    local ttoggle = iup.toggle{title = label, value = chkval;rastersize = w.."x"..h, tip = cbTTip}
    ttoggle.action = function(_,v) togcb(_,v) if v == 1 then tlist.active ="YES" else tlist.active="NO" end end
    cbTTip = nil
    return iup.hbox{ttoggle,tlist;alignment="ACENTER"}
end

function cbChatColors(profile,t)
    local enable,border,bgcolor,fgcolor = "enable", "border", "bgcolor", "fgcolor"
    local bordercolor = iup.label{title=" ";image = buildColorImage(t[border].r,t[border].g,t[border].b); rastersize="17x17"}
    local borderbtn = iup.button{title="Border";rastersize="40x21"}
    borderbtn.action=function()
        t[border].r,t[border].g,t[border].b = cbGetColor(t[border].r,t[border].g,t[border].b)
        bordercolor.image = buildColorImage(t[border].r,t[border].g,t[border].b)
        if refreshcb then refreshcb() end
        profile.modified = true
    end
    local bgc = iup.label{title=" ";image = buildColorImage(t[bgcolor].r,t[bgcolor].g,t[bgcolor].b); rastersize="17x17"}
    local bgbtn = iup.button{title="BG";rastersize="40x21"}
    bgbtn.action=function()
        t[bgcolor].r,t[bgcolor].g,t[bgcolor].b = cbGetColor(t[bgcolor].r,t[bgcolor].g,t[bgcolor].b)
        bgc.image = buildColorImage(t[bgcolor].r,t[bgcolor].g,t[bgcolor].b)
        if refreshcb then refreshcb() end
        profile.modified = true
    end
    local textcolor = iup.label{title=" ";image = buildColorImage(t[fgcolor].r,t[fgcolor].g,t[fgcolor].b); rastersize="17x17"}
    local textbtn = iup.button{title="Text";rastersize="40x21"}
    textbtn.action=function()
        t[fgcolor].r,t[fgcolor].g,t[fgcolor].b = cbGetColor(t[fgcolor].r,t[fgcolor].g,t[fgcolor].b)
        textcolor.image = buildColorImage(t[fgcolor].r,t[fgcolor].g,t[fgcolor].b)
        if refreshcb then refreshcb() end
        profile.modified = true
    end
    local refreshfunction = function()
        if t[enable] then
            borderbtn.active = "YES"
            bgbtn.active = "YES"
            textbtn.active = "YES"
        else
            borderbtn.active = "NO"
            bgbtn.active = "NO"
            textbtn.active = "NO"
        end
    end
    refreshfunction()
    local chatcolorenable = cbCheckBox("",t[enable],cbCheckBoxCB(profile,t,enable,refreshfunction),21)
    return iup.hbox{chatcolorenable,iup.frame{bordercolor;sunken="YES"; rastersize="21x21";margin="1x1"},borderbtn,
        iup.frame{bgc;sunken="YES"; rastersize="21x21";margin="1x1"},bgbtn,
        iup.frame{textcolor;sunken="YES"; rastersize="21x21";margin="1x1"},textbtn}
end

function cbReloadPowers(t)
    -- this function loads all the available click powers based on the powerset choices from the profile dialog.
    -- first start with the basic inherents that everyone can possibly have access to..
    local powerset = {"Sprint","Brawl","Rest","Prestige Power Slide","Prestige Power Rush","Prestige Power Dash","Prestige Power Surge ","Prestige Power Quick"}
    -- Next add click powers from the at primary
     for i,v in ipairs(powersets[t.archetype]["Primary"][ATPrimaries[t.atnumber][t.primaryset]]) do
         table.insert(powerset,v)
     end
    for i,v in ipairs(powersets[t.archetype]["Secondary"][ATSecondaries[t.atnumber][t.secondaryset]]) do
        table.insert(powerset,v)
    end
    if t.atnumber ~= 8 and t.atnumber ~= 12 then
        for i,v in ipairs(powersets[t.archetype]["Epic Pool"][ATEpics[t.atnumber][t.epicset]]) do
            table.insert(powerset,v)
        end
    else
        -- Handle the special case of Kheldians without Epics, but with Additional Inherent powers.
        for i,v in ipairs(powersets[t.archetype]["Inherent"]["Inherent"]) do
            table.insert(powerset,v)
        end
        for k,j in pairs(powersets[t.archetype]["Dependent"]) do
            for i,v in ipairs(j) do
                table.insert(powerset,v)
            end
        end
    end
    if t.ppset1 > 1 and t.ppset1 ~= 4 then
        for i,v in ipairs(powersets["General"]["Pool"][ATGeneral[t.atnumber][t.ppset1]]) do
            table.insert(powerset,v)
        end
    end
    if t.ppset2 > 1 and t.ppset2 ~= 4 then
        for i,v in ipairs(powersets["General"]["Pool"][ATGeneral[t.atnumber][t.ppset2]]) do
            table.insert(powerset,v)
        end
    end
    if t.ppset3 > 1 and t.ppset3 ~= 4 then
        for i,v in ipairs(powersets["General"]["Pool"][ATGeneral[t.atnumber][t.ppset3]]) do
            table.insert(powerset,v)
        end
    end
    if t.ppset4 > 1 and t.ppset4 ~= 4 then
        for i,v in ipairs(powersets["General"]["Pool"][ATGeneral[t.atnumber][t.ppset4]]) do
            table.insert(powerset,v)
        end
    end
    table.insert(powerset,"Eye of the Magus")
    table.insert(powerset,"Crey CBX-9 Pistol")
    table.insert(powerset,"Gaes of the Kind Ones")
    table.insert(powerset,"Vanguard Medal")
    t.powerset = powerset
end

"""
