# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class mainWindow
###########################################################################

class mainWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AutoSIEM - Load and Analyze log files.", pos = wx.DefaultPosition, size = wx.Size( 1587,685 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.m_filePicker = wx.FilePickerCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 500,-1 ), wx.FLP_DEFAULT_STYLE )
		self.m_filePicker.Hide()
		
		self.m_toolBar1.AddControl( self.m_filePicker )
		self.m_buttonAnalyze = wx.Button( self.m_toolBar1, wx.ID_ANY, u"Analyze Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_buttonAnalyze )
		self.m_textCtrl = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_textCtrl )
		self.m_toolBar1.AddSeparator()
		
		self.m_toolBar1.AddSeparator()
		
		self.m_toolBar1.AddSeparator()
		
		self.m_toolBar1.AddSeparator()
		
		self.m_toolBar1.AddSeparator()
		
		self.m_staticText1 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"Sort By: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText1 )
		m_comboBoxSortChoices = [ u"Timestamps", u"sID", u"Category", u"Classification", u"Priority", u"Protocol", u"Source IP", u"Source Port", u"Destination IP", u"Destination Port", u"Importance" ]
		self.m_comboBoxSort = wx.ComboBox( self.m_toolBar1, wx.ID_ANY, u"Timestamps", wx.DefaultPosition, wx.DefaultSize, m_comboBoxSortChoices, 0 )
		self.m_comboBoxSort.SetSelection( 0 )
		self.m_toolBar1.AddControl( self.m_comboBoxSort )
		self.m_sortButton = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"sort", wx.Bitmap( u"SortButton.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_sortButton1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"sort", wx.Bitmap( u"SortButtonDesc.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_gridList = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_gridList.CreateGrid( 200, 11 )
		self.m_gridList.EnableEditing( True )
		self.m_gridList.EnableGridLines( True )
		self.m_gridList.EnableDragGridSize( False )
		self.m_gridList.SetMargins( 2, 0 )
		
		# Columns
		self.m_gridList.SetColSize( 0, 92 )
		self.m_gridList.SetColSize( 1, 84 )
		self.m_gridList.SetColSize( 2, 603 )
		self.m_gridList.SetColSize( 3, 271 )
		self.m_gridList.SetColSize( 4, 61 )
		self.m_gridList.SetColSize( 5, 55 )
		self.m_gridList.SetColSize( 6, 161 )
		self.m_gridList.SetColSize( 7, 110 )
		self.m_gridList.SetColSize( 8, 115 )
		self.m_gridList.SetColSize( 9, 104 )
		self.m_gridList.SetColSize( 10, 80 )
		self.m_gridList.EnableDragColMove( False )
		self.m_gridList.EnableDragColSize( True )
		self.m_gridList.SetColLabelSize( 30 )
		self.m_gridList.SetColLabelValue( 0, u"Time" )
		self.m_gridList.SetColLabelValue( 1, u"Signature" )
		self.m_gridList.SetColLabelValue( 2, u"Category" )
		self.m_gridList.SetColLabelValue( 3, u"Classification" )
		self.m_gridList.SetColLabelValue( 4, u"Priority" )
		self.m_gridList.SetColLabelValue( 5, u"Protocol" )
		self.m_gridList.SetColLabelValue( 6, u"Source IP" )
		self.m_gridList.SetColLabelValue( 7, u"Source Port" )
		self.m_gridList.SetColLabelValue( 8, u"Destination IP" )
		self.m_gridList.SetColLabelValue( 9, u"Destination Port" )
		self.m_gridList.SetColLabelValue( 10, u"Importance" )
		self.m_gridList.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_gridList.AutoSizeRows()
		self.m_gridList.EnableDragRowSize( True )
		self.m_gridList.SetRowLabelSize( 100 )
		self.m_gridList.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_gridList.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer1.Add( self.m_gridList, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar2 = wx.MenuBar( 0 )
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonAnalyze.Bind( wx.EVT_BUTTON, self.readLog )
		self.Bind( wx.EVT_TOOL, self.SortAscend, id = self.m_sortButton.GetId() )
		self.Bind( wx.EVT_TOOL, self.SortDescend, id = self.m_sortButton1.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def readLog( self, event ):
		event.Skip()
	
	def SortAscend( self, event ):
		event.Skip()
	
	def SortDescend( self, event ):
		event.Skip()
	

