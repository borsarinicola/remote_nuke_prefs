'''
This file contains custom preferences, presets and keyboard shortcut for nuke
'''

import nuke, sys, os, subprocess


###################################


#add defaults


#default preferences
nuke.toNode('preferences')['LocalizationPauseOnProjectLoad'].setValue(True)
nuke.toNode('preferences')['maxPanels'].setValue(1)
nuke.toNode('preferences')['GridHeight'].setValue(50)
nuke.toNode('preferences')['dag_snap_threshold'].setValue(10)
nuke.toNode('preferences')['ArrowColorUp'].setValue(0xff0000ff)



#default projects settings
nuke.knobDefault('Root.project_directory', '[python {nuke.script_directory()}]')
nuke.knobDefault('Root.format', 'HD_1080')
nuke.knobDefault('Root.first_frame', '1001')
nuke.knobDefault('Root.last_frame', '1100')
nuke.knobDefault('Root.fps', '25')



# personal default knobs values
nuke.knobDefault('Shuffle.label','[value in]_[value out]')
nuke.knobDefault('ShuffleCopy.label','[value in]_[value out]')
nuke.knobDefault('LayerContactSheet.showLayerNames', 'True')
nuke.knobDefault('Remove.channels','alpha')
nuke.knobDefault('AppendClip.firstFrame','1001')
#nuke.knobDefault('Merge2.bbox','B')
#nuke.knobDefault('ChannelMerge.bbox','B side')
nuke.knobDefault('Write.create_directories', 'True')
#nuke.knobDefault("Write.exr.compression","4")   #RLE as default EXR compression
nuke.knobDefault("EXPTool.mode", "0")   #Stops as default Exposure Parameter
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')



#create keep function add it to the channel menu
def createkeep():
	nuke.createNode('Remove')
	rem = nuke.selectedNode()
	rem.knob('operation').setValue('keep')
	rem.knob('channels').setValue('rgba')
	return
nuke.menu('Nodes').addCommand( "Channel/Keep", "createkeep()", icon="Remove.png")
nuke.menu('Nodes').addCommand( "Filter/Dilate", "nuke.createNode('Dilate')", icon="ErodeFast.png")
nuke.menu('Nodes').addCommand( "Merge/PSDMerge", "nuke.createNode('PSDMerge')", icon="Merge.png")



#add custom resolutions to format list

DCP_2K_Full = '2048 1152 DCP_2K_Full'
nuke.addFormat(DCP_2K_Full)

DCP_2K_Scope = '2048 858 DCP_2K_Scope'
nuke.addFormat(DCP_2K_Scope)

DCP_2K_Flat = '1998 1080 DCP_2K_Flat'
nuke.addFormat(DCP_2K_Flat)



####################################


# custom shortcuts

toolbar = nuke.menu('Nodes')
toolbar.addCommand('Merge/KeyMix', 'nuke.createNode("Keymix")', 'v')
toolbar.addCommand('Color/Math/Expression', 'nuke.createNode("Expression")', 'e')
toolbar.addCommand('Color/Invert', 'nuke.createNode("Invert")', 'alt+ctrl+i')
toolbar.addCommand('Merge/Premult', 'nuke.createNode("Premult")', 'alt+shift+p')
toolbar.addCommand('Merge/Unpremult', 'nuke.createNode("Unpremult")', 'alt+shift+u')
toolbar.addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+m')
toolbar.addCommand('Transform/TransformMasked', 'nuke.createNode("TransformMasked")', 'shift+t')
toolbar.addCommand('Channel/Shuffle', 'nuke.createNode("Shuffle1")', index=0, icon='Shuffle.png')
toolbar.addCommand('Channel/ShuffleCopy', 'nuke.createNode("ShuffleCopy")', index=1, icon='ShuffleCopy.png')


# ####################################


# add nodes presets

nuke.setUserPreset("Expression", "Binary Alpha - Fringe to 1", {'expr3': 'a>0?1:0', 'selected': 'true', 'label': '[value expr3]'})
nuke.setUserPreset("Expression", "Binary Alpha - Fringe to 0", {'expr3': 'a<1?0:1', 'selected': 'true', 'label': '[value expr3]'})
nuke.setUserPreset("Expression", "STMap", {'expr0': '(x+0.5)/width', 'expr1': '(y+0.5)/height', 'selected': 'true', 'label': 'STMap'})
nuke.setUserPreset("Expression", "Channels to Alpha", {'selected': 'true', 'temp_name2': 'GB', 'temp_name3': 'RGB', 'temp_name0': 'RG', 'temp_name1': 'RB', 'expr3': 'RGB', 'temp_expr2': 'g+b-(g*b)', 'temp_expr3': 'RG+b-(RG*b)', 'temp_expr0': 'r+g-(r*g)', 'temp_expr1': 'r+b-(r*b)'})
nuke.setUserPreset("MergeExpression", "Alpha Disjoint-Over", {'temp_name0': 'a', 'selected': 'true', 'expr0': 'A.a+B.a<1?A.a+B.a:B.a==0?A.a:a', 'label': 'Alpha Disjoint-Over', 'channel3': 'none', 'channel2': 'none', 'channel1': 'none', 'channel0': 'alpha', 'temp_expr0': 'A.a+B.a*(1-A.a)/B.a'})
nuke.setUserPreset("ColorMatrix", "LMT Hilights Staturation Fix", {'selected': 'true', 'matrix': ' {0.9404372683 -0.0183068787 0.0778696104} {0.0083786969 0.8286599939 0.1629613092} {0.0005471261 -0.0008833746 1.000336249}'})


# ####################################


# add custom functions to menus

menubar = nuke.menu('Nuke')



def restartNuke():

    if nuke.ask('Are you sure you want to restart Nuke?'):

        scriptName = nuke.root().knob('name').getValue() 

        subprocess_options = {
            "shell": True
            }
        
        separate_terminal_options = {
           "close_fds": True,
           "preexec_fn": os.setsid
           }

        if nuke.env['nukex'] == True:
            session = '--nukex'
        else:
            session = '--nuke'


        if 'REZ_VOLT_SESSION_ROOT' in os.environ:
            subprocess_options.update(separate_terminal_options)

        if os.path.isfile(scriptName):
            nuke.scriptSave()
            launch_cmd = '{} {} {}'.format(sys.executable, session, scriptName)
            subprocess.Popen(launch_cmd, **subprocess_options)
            nuke.modified(False)
            nuke.scriptExit()
        else:
            nuke.scriptNew('')
            nuke.modified(False)
            nuke.scriptExit()
			

menubar.addCommand('File/Restart Nuke', 'restartNuke()', 'alt+shift+q', icon='', index=5) # add option that restart nuke
menubar.addCommand('Edit/Autocrop Selected Nodes','nukescripts.autocrop()') # add gizmo to group conversion - importing it when in use


def bbox2b(side):
    for node in nuke.selectedNodes():
        try:
            node['bbox'].setValue(side)
        except:
            pass

menubar.addCommand('Edit/Set Nodes BBox/to A', 'bbox2b(side="A")', 'shift+a')
menubar.addCommand('Edit/Set Nodes BBox/to B', 'bbox2b(side="B")', 'shift+b')
menubar.addCommand('Edit/Set Nodes BBox/to Union', 'bbox2b(side="union")', 'shift+u')


def closeProperties():
    [node.hideControlPanel() for node in nuke.allNodes(recurseGroups=True)]

menubar.addCommand('Edit/Close Nodes Properties', 'closeProperties()', '`')


######################################

#add grade control to CurveTool

def addCTGradeControl():
    node = nuke.thisNode()
    tab = nuke.Tab_Knob('GradeControl')
    node.addKnob(tab)

    ref = nuke.Int_Knob('reference_frame', 'Reference Fame')
    frame = nuke.PyScript_Knob('set_frame', 'Set Current Frame', 'nuke.thisNode()["reference_frame"].setValue(nuke.frame())')
    node['label'].setValue('Ref [value reference_frame]')
    grade = nuke.PyScript_Knob('create_grade', 'Create Grade Node', '''

node = nuke.thisNode()
node_name = nuke.thisNode()['name'].value()
grade = nuke.createNode('Grade')
grade['whitepoint'].setSingleValue(False)
grade['white'].setSingleValue(False)
grade['whitepoint'].setExpression('{0}.intensitydata.r({0}.reference_frame)'.format(node_name), channel=0)
grade['whitepoint'].setExpression('{0}.intensitydata.g({0}.reference_frame)'.format(node_name), channel=1)
grade['whitepoint'].setExpression('{0}.intensitydata.b({0}.reference_frame)'.format(node_name), channel=2)
grade['whitepoint'].setExpression('{0}.intensitydata.a({0}.reference_frame)'.format(node_name), channel=3)
grade['white'].setExpression('{0}.intensitydata.r'.format(node_name), channel=0)
grade['white'].setExpression('{0}.intensitydata.g'.format(node_name), channel=1)
grade['white'].setExpression('{0}.intensitydata.b'.format(node_name), channel=2)
grade['white'].setExpression('{0}.intensitydata.a'.format(node_name), channel=3)

    ''')

    grade.setFlag(0x1000)
    node.addKnob(ref)
    node.addKnob(frame)
    node.addKnob(grade)
    node['reference_frame'].setValue(nuke.frame())


nuke.addOnCreate(addCTGradeControl, nodeClass='CurveTool')
