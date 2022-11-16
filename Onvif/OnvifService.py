from onvif import ONVIFCamera
import zeep
import asyncio
import json
from Onvif.OnvifRequest import OnvifRequest
from Onvif.OnvifPtz import *

class OnvifClass():
    def __init__(self) -> None:
        print("Created OnvifCalss!!")
        #self.setup()
        self.isOnvifCamera = False
        self.isSetMediaService = False
        self.isSetPtzService = False
        self.isSetAnalyticService = False
        self.isSetDeviceIOService = False
        self.isSetDeviceMgmtService = False
        self.isSetImagingService = False
        self.isSetReplayService = False
        self.isSetReceiverService = False
        self.isSetEventsService = False
        self.isSetRecordingService = False
        self.isSetPullpointService = False
        self.isSetOnvifService = False
        
        self.isSetRequestStop = False
        self.isSetRequestCont = False

    XMAX = 1
    XMIN = -1
    YMAX = 1
    YMIN = -1

    __onvifPtzProtocol = False
    
    def setupOnvifCamera(self, ipAddress, port, id, pw):
        try:
            self.mycam = ONVIFCamera(ipAddress, port, id, pw)
            # Alternative Request for SOAP onvif operation
            self.onvifRequest = OnvifRequest(id, pw) 
            self.isOnvifCamera = True
            self.mycam.update_xaddrs()
            self.services = self.mycam.use_services_template
        except Exception as e:
            print("Exception raised in setupOnvifCamera : ", e)
    
    def setupMedia(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create media service object
            self.media = self.mycam.create_media_service()
            self.isSetMediaService = True
            # Get target profile
            self.media_profiles = self.media.GetProfiles()
            #print(self.media_profiles)
            self.media_profile = self.media.GetProfiles()[0]

        except Exception as e:
            print("Exception raised in setupMedia : ", e)
            
    def setupAnalytics(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create analytics service object
            self.analytics = self.mycam.create_analytics_service()
            self.isSetAnalyticService = True
            self.analytics_capabilities = self.analytics.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupAnalytics : ", e)
            
    def setupDeviceIO(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create deviceIO service object
            self.deviceIO = self.mycam.create_deviceio_service()
            self.isSetDeviceIOService = True
            self.deviceIO_capabilities = self.deviceIO.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceIO : ", e)
            
    def setupDeviceMgmt(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create DeviceMgmt service object
            self.deviceMgmt = self.mycam.create_devicemgmt_service()
            self.isSetDeviceMgmtService = True
            self.deviceMgmt_capabilities = self.deviceMgmt.GetCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceMgmt : ", e)
    
    def setupImaging(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create imaging service object
            self.imaging = self.mycam.create_imaging_service()
            self.isSetImagingService = True
            self.imaging_capabilities = self.imaging.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupDeviceIO : ", e)
    
    def setupReplay(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create replay service object
            self.replay = self.mycam.create_replay_service()
            self.isSetReplayService = True
            self.replay_capabilities = self.replay.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupReplay : ", e)
    
    def setupReceiver(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create receiver service object
            self.receiver = self.mycam.create_receiver_service()
            self.isSetReceiverService = True
            self.receiver_capabilities = self.receiver.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupReceiver : ", e)
    
    def setupEvents(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create event service object
            self.events = self.mycam.create_events_service()
            self.isSetEventsService = True
            self.events_capabilities = self.events.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupEvent : ", e)
    
    def setupRecording(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.recording = self.mycam.create_recording_service()
            self.isSetRecordingService = True
            self.recording_capabilities = self.recording.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupRecording : ", e)
            
    def setupPullpoint(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.pullpoint = self.mycam.create_pullpoint_service()
            self.isSetPullpointService = True
            self.pullpoint_capabilities = self.pullpoint.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupPullpoint : ", e)
    
    def setupOnvif(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create recording service object
            self.onvif = self.mycam.create_onvif_service()
            self.isSetOnvifService = True
            self.onvif_capabilities = self.onvif.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupOnvif : ", e)
    
    def setupPtz(self):
        try:
            if not self.isOnvifCamera:
                return
            
            # Create ptz service object
            self.ptz = self.mycam.create_ptz_service()
            self.isSetPtzService = True
            self.ptz_capabilities = self.ptz.GetServiceCapabilities()
        except Exception as e:
            print("Exception raised in setupPtz : ", e)
    
    def setup(self, data):
        try:
            ipAddress = data["onvif"]["ip_address"]
            port = str(data["onvif"]["port"])
            id = data["onvif"]["id"]
            pw = data["onvif"]["password"]
            # self.mycam = ONVIFCamera(ipAddress, port, id, pw)
            # self.onvifRequest = OnvifRequest(id, pw)
            self.setupOnvifCamera(ipAddress, port, id, pw)
            self.createServices()
            self.setupPtzOperation()
        except Exception as e:
            print("Exception raised when parsing Data in setup : ", e)
       
        try:
            # Get zeep_pythonvalue
            zeep.xsd.simple.AnySimpleType.pythonvalue = self.zeep_pythonvalue
        except Exception as e:
            print("Raised an exception during zeep_pythonvalue : ", e)
       
       
    def createServices(self):
        for key, value in self.services.items():
            service = key.lower()
            #print(self.mycam.xaddrs)
            print(service, value)
            if service == 'devicemgmt':
                self.setupDeviceMgmt()
            elif service == 'ptz':
                self.setupPtz()
            elif service == 'media':
                self.setupMedia()
            elif service == 'imaging':
                self.setupImaging()
            elif service == 'events':
                self.setupEvents
            elif service == 'analytics':
                self.setupAnalytics()
            elif service == 'deviceio':
                self.setupDeviceIO()
            elif service == 'recording':
                self.setupRecording()
            elif service == 'receiver':
                self.setupReceiver()
            elif service == 'replay':
                self.setupReplay()
            elif service == 'onvif':
                self.setupOnvif()
            elif service == 'pullpoint':
                self.setupPullpoint()
    
    def setupPtzOperation(self):
        try:
            self.getPTZConfigOption()
            self.createPTZContReq()
            self.createPTZStopReq()
            self.setPTZContVelocity()
            self.ptzContTest()
        except Exception as e:
            print("Raised an exception during setupPtzOperation : ", e)
    
    def getPTZConfigOption(self):
        try:
            # Get PTZ configuration options for getting continuous move range
            self.request_ptzOption = self.ptz.create_type('GetConfigurationOptions')
            self.request_ptzOption.ConfigurationToken = self.media_profile.PTZConfiguration.token
            self.ptz_configuration_options = self.ptz.GetConfigurationOptions(self.request_ptzOption)
            #print('PTZ configuration options:', self.ptz_configuration_options)
            
            self.setMax()
            
        except Exception as e:
            print("Raised an exception during getPTZConfigOption : ", e)
    
    def setPTZContVelocity(self):
        try:
            self.request_continuousMove.Velocity = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position
            self.request_continuousMove.Velocity.PanTilt.space = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            self.request_continuousMove.Velocity.Zoom.space = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI
        except Exception as e:
            self.request_continuousMove.Velocity  = Velocity()
            print("Raised an exception during setPTZContVelocity : ", e)

    def setPTZStopStatus(self):
        try:
            self.request_stop.PanTilt = True
            self.request_stop.Zoom = True
            self.request_stop.ProfileToken = self.media_profile.token
        except Exception as e:
            print("Raised an exception during setPTZStopStatus : ", e)

    def setMax(self):
        # Get range of pan and tilt
        # NOTE: X and Y are velocity vector
        try:
            self.XMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
            self.XMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
            self.YMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
            self.YMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
        except Exception as e:
            print("Raised an exception during setMax : ", e)
    
    def createPTZContReq(self):
        try:
            
            #Set Continuous request
            self.request_continuousMove = self.ptz.create_type('ContinuousMove')
            self.request_continuousMove.ProfileToken = self.media_profile.token
            self.setPTZContVelocity()
        except Exception as e:
            print("Raised an exception during createPTZContReq : ", e)
            
    def createPTZStopReq(self):
        try:
            #Set Ptz stop
            self.request_stop = self.ptz.create_type('Stop')
            self.isSetRequestStop = True
            self.setPTZStopStatus()
            
        except Exception as e:
            print("Raised an exception during createPTZStopReq : ", e)
    
    def ptzContTest(self):
        try:
            self.ptz.Stop(self.request_stop)
            self.__onvifPtzProtocol = True
            
        except Exception as e:
            self.onvifRequest.setPtzXaddr(self.ptz)
            self.__onvifPtzProtocol = False
            print("Raised an exception during ptzContTest : ", e)
       
    def getRtspUri(self):
        try:
            self.obj = self.media.create_type('GetStreamUri')
            self.obj.ProfileToken = self.media_profile.token
            self.obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
            #print(self.media.GetStreamUri(self.obj)["Uri"])
            return self.media.GetStreamUri(self.obj)["Uri"]
        
        except Exception as e:
            print("Raised an exception during getRtspUri : ", e)
            
    
            
    
    def getStreamingUrl(self):
        print(self.request_continuousMove)
        
    
    def zeep_pythonvalue(self, xmlvalue):
        return xmlvalue

        
    def moveUp_pressDonw(self):
        try:
            self.request_continuousMove.Velocity.Zoom.x = 0
            self.request_continuousMove.Velocity.PanTilt.x = 0
            self.request_continuousMove.Velocity.PanTilt.y = self.YMAX
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            print("Raised Exception in moveUp_pressDonw : ", e)
            
        
    def moveDown_pressDown(self):
        try:
            self.request_continuousMove.Velocity.Zoom.x = 0
            self.request_continuousMove.Velocity.PanTilt.x = 0
            self.request_continuousMove.Velocity.PanTilt.y = self.YMIN
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            
            print("Raised Exception in moveDown_pressDown : ", e)
            
    
    def moveRight_pressDonw(self):
        try:
            self.request_continuousMove.Velocity.Zoom.x = 0
            self.request_continuousMove.Velocity.PanTilt.x = self.XMAX
            self.request_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            print("Raised Exception in moveRight_pressDonw : ", e)
            
    
    def moveLeft_pressDonw(self):
        try:
            self.request_continuousMove.Velocity.Zoom.x = 0
            self.request_continuousMove.Velocity.PanTilt.x = self.XMIN
            self.request_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            print("Raised Exception in moveLeft_pressDonw : ", e)
            
    
    def zoomOut_pressDown(self):
        try:
            print('zoom down')
            self.request_continuousMove.Velocity.Zoom.x = -1
            self.request_continuousMove.Velocity.PanTilt.x = 0
            self.request_continuousMove.Velocity.PanTilt.y = 0
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            print("Raised Exception in zoomOut_pressDown : ", e)
            
        
    def zoomUp_pressDown(self):
        try:
            
            self.request_continuousMove.Velocity.Zoom.x = 1
            self.request_continuousMove.Velocity.PanTilt.x = 0
            self.request_continuousMove.Velocity.PanTilt.y = 0
            print('zoom_pressDown')
            # Start continuous move
            if self.__onvifPtzProtocol:
                self.ptz.ContinuousMove(self.request_continuousMove)
            else:
                self.onvifRequest.ContinuousMove(self.request_continuousMove)
        except Exception as e:
            print("Raised Exception in zoomUp_pressDown : ", e)
            
    
    def btnReleased(self):
        try:
            print('button released')
            #self.ptz.Stop({'ProfileToken': self.request.ProfileToken})
            if self.__onvifPtzProtocol:
                self.ptz.Stop(self.request_stop)
            else:
                self.onvifRequest.Stop(self.request_stop)
        except Exception as e:
            print("Raised Exception in btnReleased : ", e)
            