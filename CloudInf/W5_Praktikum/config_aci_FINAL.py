#
#   WELCOME TO AWESOME SCRIPT v1.0
#   ------------------------------
#   we have decided to initialize all variables at the start of the script
#   (so the script want ask the user at every step about the names etc.)
#
#

import urllib3.contrib.pyopenssl
import cobra.mit.request
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.model import pol, phys, infra, fvns, aaa, fv, vz, dhcp

# is needed else a ssl error occurs
urllib3.disable_warnings()

#Initialize variables
####################
tenantName = 'group10'

#vlanPool1
vlanName1 = 'Group10-VLAN510'
vlanDescr1 = ''

#vlanPool2
vlanName2 = 'Group10-VLAN710'
vlanDescr2 = ''

#EncapBlock1
encapFrom1 = '510'
encapTo1 = '510'
encapType1 = 'static'

#EncapBlock2
encapFrom2 = '710'
encapTo2 = '710'
encapType2 = 'static'

#physical Domain 1
physDomName1 = 'Group10-DOMAIN-GREEN'
physDomRef1 = 'group10'

#physical Domain 2
physDomName2 = 'Group10-DOMAIN-RED'
physDomRef2 = 'group10'

#AAEP1
aaepName1 = 'Group10-AAEP-GREEN'
aaepDescr1 = ''


#AAEP2
aaepName2 = 'Group10-AAEP-RED'
aaepDescr2 = ''

#PolGroup1
polName1 = 'Group10-POLGROUP-GREEN'
polDescr1 = ''

#PolGroup2
polName2 = 'Group10-POLGROUP-RED'
polDescr2 = ''

#PortInterface1
polIntName1 = 'Group10-INTPROFILE-GREEN'
polIntDescr1 = ''

#PortInterface2
polIntName2 = 'Group10-INTPROFILE-RED'
polIntDescr2 = ''

#PortAssignement1
portName1 = 'e1-14'
portDescr1 = ''
fromPort1 = '14'
toPort1 = '14'

#PortAssignement2
portName2 = 'e1-29'
portDescr2 = ''
fromPort2 = '29'
toPort2 = '29'

#Switch Profile 1
switchProfileName1 = 'Group10-Leaf1-Leaf2'
leafSelectorTo1 = '102'
leafSelectorFrom1 = '101'

#Switch Profile 2
switchProfileName2 = 'Group10-Leaf2'
leafSelectorTo2 = '102'
leafSelectorFrom2 = '102'

#BridgeDomain
macAddr = '00:22:BD:F8:19:FF'
bdName = 'green-red_BD'
ipAdd = '192.168.10.1/24'

#Application Profile
appName = 'green-red'
appDescr = 'Application Profile Group10'

#EPG1
nameEPG1 = 'green_EPG'

#EPG2
nameEPG2 = 'red_EPG'

#Contract
contName = 'green_to_red'
contDesc = ''
contAction = 'permit'



def getUserName():
    username = raw_input('Enter loginName: ')
    return username


def getPassword():
    password = raw_input('Enter password: ')
    return password

def getIP():
    ip = raw_input('Enter IP-Address of Controller [Format: x.x.x.x]: ')
    return ip


def getURL():
    return 'https://%s/' % (getIP())


def createLoginSession():
    return LoginSession(getURL(), getUserName(), getPassword())


def createVLANPoolSTATIC(infraObj, name, descr):
    print('CREATING VLANPOOL')
    return cobra.model.fvns.VlanInstP(infraObj,
                                      name=name,
                                      descr=descr,
                                      allocMode='static')


def addEncapBlockSTATIC(vlanPool, rangeFrom, rangeTo):
    print('ADDING VLAN ENCAP BLOCK')
    return cobra.model.fvns.EncapBlk(vlanPool,
                                     from_='vlan-' + rangeFrom,
                                     to='vlan-' + rangeTo,
                                     allocMode='static')


def commit(modifiedObj, rootObj):
    print('Commiting changes...')

    modification = cobra.mit.request.ConfigRequest()
    modification.addMo(modifiedObj)
    rootObj.commit(modification)


def createPhysDomain(rootObj, domName, refName, vlanName):
    print('CREATING PHYSICAL DOMAIN')

    physDom = cobra.model.phys.DomP(rootObj, name=domName)
    domRef = cobra.model.aaa.DomainRef(physDom, name=refName)
    domVlan = cobra.model.infra.RsVlanNs(physDom,
                                         tDn='uni/infra/vlanns-['+vlanName+']-static')

def createAAEP(infraObj, name, descr, domName):
    print('CREATING AAEP')

    infraAAEP = cobra.model.infra.AttEntityP(infraObj,
                                             name=name,
                                             descr=descr)

    domRef = cobra.model.infra.RsDomP(infraAAEP, tDn=u'uni/phys-'+domName)

    return infraAAEP



#simlyfied method which adds all necessary options
def createPolGroupVPC(infraFunc, name, descr):
    print('CREATING POLGROUP VPC')


    polGroup = cobra.model.infra.AccBndlGrp(infraFunc,
                                            name=name,
                                            descr=descr,
                                            lagT=u'node')

    cobra.model.infra.RsLacpPol(polGroup, tnLacpLagPolName=u'LACP')
    cobra.model.infra.RsCdpIfPol(polGroup, tnCdpIfPolName=u'CDP_ON')
    cobra.model.infra.RsAttEntP(polGroup, tDn=u'uni/infra/attentp-'+aaepName1)

    return polGroup

def createPolGroupLeafAccessPort(infraFunc, name, descr):
    print('CREATING POLGROUP LEAF ACCESS PORT')

    polGroup = cobra.model.infra.AccPortGrp(infraFunc,
                                            name=name,
                                            descr=descr)

    cobra.model.infra.RsCdpIfPol(polGroup, tnCdpIfPolName=u'CDP_ON')
    cobra.model.infra.RsLldpIfPol(polGroup, tnLldpIfPolName=u'LLDP_ON')
    cobra.model.infra.RsAttEntP(polGroup, tDn=u'uni/infra/attentp-'+aaepName2)

    return polGroup

def createPortInterfaceProfile(infraObj, name, descr):
    print('CREATING PORT INT PROFILE')

    portIntProfile = cobra.model.infra.AccPortP(infraObj,
                                                name=name,
                                                descr=descr)

    return portIntProfile

def assignPortToInt(interface, name, descr, fromPort, toPort, polGroupName):
    print('ASSIGN PORT TO INTERFACE')

    infraHPortS = cobra.model.infra.HPortS(interface,
                                           name=name,
                                           descr=descr,
                                           type=u'range')

    cobra.model.infra.PortBlk(infraHPortS,
                              name=u'block2',
                              fromPort=fromPort,
                              toPort=toPort)

    cobra.model.infra.RsAccBaseGrp(infraHPortS,
                                   tDn=u'uni/infra/funcprof/accbundle-'+polGroupName)

def assignPortToIntPortGrp(interface, name, descr, fromPort, toPort, polGroupName):
    print('ASSIGN PORT TO INTERFACE')

    infraHPortS = cobra.model.infra.HPortS(interface,
                                           name=name,
                                           descr=descr,
                                           type=u'range')

    cobra.model.infra.PortBlk(infraHPortS,
                              name=u'block2',
                              fromPort=fromPort,
                              toPort=toPort)

    cobra.model.infra.RsAccBaseGrp(infraHPortS,
                                   tDn=u'uni/infra/funcprof/accportgrp-'+polGroupName)


def createSwitchProfile(infraObj, name):
    print('CREATING SWITCH PROFILE')

    return cobra.model.infra.NodeP(infraObj, name=name)

def addLeafSelectorsVPC(switchProfile, interfaceProfileName, leafTo, leafFrom):
    print('ADD LEAF SELECTOR VPC')

    infraRsAccPortPGreen = cobra.model.infra.RsAccPortP(switchProfile,
                                                        tDn=u'uni/infra/accportprof-'+interfaceProfileName)

    infraLeafSGreen = cobra.model.infra.LeafS(switchProfile, type=u'range', name=u'VPC')

    infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafSGreen, to_=leafTo, from_=leafFrom, name=u'2314c722b8025597')

def addLeafSelectorsLeafAccessPort(switchProfile, interfaceProfileName, leafTo, leafFrom):
    print('ADD LEAF SELECTOR LEAF ACCESS PORT')

    infraRsAccPortPRed = cobra.model.infra.RsAccPortP(switchProfile,
                                                      tDn=u'uni/infra/accportprof-'+interfaceProfileName)
    infraLeafSRed = cobra.model.infra.LeafS(switchProfile, type=u'range', name=u'LeafAccessPort')
    infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafSRed, to_=leafTo, from_=leafFrom, name=u'2d3e0d4a8657de19')


def createBridgeDomain(rootObj, tenantName, macAddr, name, ipAddr):
    print('CREATING BRIDGE DOMAIN')
    fvTenant = cobra.model.fv.Tenant(rootObj, tenantName)
    fvBD = cobra.model.fv.BD(fvTenant, mac=macAddr, name=name)
    fvSubnet = cobra.model.fv.Subnet(fvBD, ip=ipAddr, ctrl=u'unspecified')
    fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=u'default')

    return fvBD

def createApplicationProfile(rootObj, infraObj, appName, tenantName, descr):
    print('CREATING APPLICATION PROFLE')
    infraFuncP = cobra.model.infra.FuncP(infraObj)
    infraAccPortGrp = cobra.model.infra.AccPortGrp(infraFuncP, name=u'ApplicationProfile',
                                                   descr=descr)
    infraRsL2PortAuthPol = cobra.model.infra.RsL2PortAuthPol(infraAccPortGrp)
    fvTenant = cobra.model.fv.Tenant(rootObj, tenantName)
    fvAp = cobra.model.fv.Ap(fvTenant, name=appName)
    return fvAp

def createEPG(applicationProfile, name):
    print('CREATING APPLICATION PROFILE')
    appProfile = cobra.model.fv.AEPg(applicationProfile, name=name)
    return appProfile

def addDomainToEPG(epg, name, domain):
    print('ADDING DOMAIN TO EPG')
    fvRsBd = cobra.model.fv.RsBd(epg, tnFvBDName=name)
    fvRsDomAtt = cobra.model.fv.RsDomAtt(epg, tDn=u'uni/phys-'+domain, resImedcy=u'immediate')

def mapPhysicalPortPolGroup(epg, polgroupName):
    fvRsPathAtt = cobra.model.fv.RsPathAtt(epg,
                                           tDn=u'topology/pod-1/protpaths-101-102/pathep-'+polgroupName,
                                           encap=u'vlan-510')

def mapPhysicalPortPort(egp):
    fvRsPathAtt = cobra.model.fv.RsPathAtt(egp,
                                           tDn=u'topology/pod-1/paths-102/pathep-[eth1/29]',
                                           encap=u'vlan-710')


def getTenant(rootObj, tenantName):
    return cobra.model.fv.Tenant(rootObj, tenantName)

def addDHCP(bridgeDomain):
    dhcpLbl = cobra.model.dhcp.Lbl(bridgeDomain, name=u'Blue-DHCP')

def main():
    print('Welcome to the awesome ACI Python script')
    print('Login Information needed...')

    session = createLoginSession()

    # create directory object and login
    directoryObj = MoDirectory(session)
    directoryObj.login()

    print('Successfully logged in')
    print('----------------------')

    # create root object
    rootObj = cobra.model.pol.Uni('')
    infraObj = cobra.model.infra.Infra(rootObj)
    infraFunc = cobra.model.infra.FuncP(infraObj)
    tenant = getTenant(rootObj, tenantName)

    # 1.0 Creating vlanPools and EncapBlocks
    vlanPoolServerGreen = createVLANPoolSTATIC(infraObj, vlanName1, vlanDescr1)
    addEncapBlockSTATIC(vlanPoolServerGreen, encapFrom1, encapTo1)

    vlanPoolServerRed = createVLANPoolSTATIC(infraObj, vlanName2, vlanDescr2)
    addEncapBlockSTATIC(vlanPoolServerRed, encapFrom2, encapTo2)

    commit(infraObj, directoryObj)
    commit(vlanPoolServerGreen, directoryObj)
    commit(vlanPoolServerRed, directoryObj)

    # 2.0 Creating physical Domain
    physDomGreen = createPhysDomain(rootObj, physDomName1, physDomRef1, vlanName1)
    physDomGreen = createPhysDomain(rootObj, physDomName2, physDomRef2, vlanName2)
    commit(rootObj, directoryObj)

    # 3.0 Create AAEP
    aaepGreen = createAAEP(infraObj, aaepName1, aaepDescr1, physDomName1)
    aaepRed = createAAEP(infraObj, aaepName2, aaepDescr2, physDomName2)
    commit(infraObj, directoryObj)

    # 4.0 Create Policy Groups
    polGroupGreen = createPolGroupVPC(infraFunc, polName1, polDescr1)
    polGroupred = createPolGroupLeafAccessPort(infraFunc, polName2, polDescr2)

    commit(infraFunc, directoryObj)

    #5.0 Create Port Interface
    portIntProfilGreen = createPortInterfaceProfile(infraObj, polIntName1, polIntDescr1)
    portIntProfilRed = createPortInterfaceProfile(infraObj, polIntName2, polIntDescr2)

    #5.1 Assign Port to Interface
    assignPortToInt(portIntProfilGreen, portName1, portDescr1, fromPort1, toPort1, polName1)
    assignPortToIntPortGrp(portIntProfilRed, portName2, portDescr2, fromPort2, toPort2, polName2)

    commit(infraObj, directoryObj)
    commit(portIntProfilGreen, directoryObj)
    commit(portIntProfilRed, directoryObj)

    #6.0 Create Switch Profiles
    switchProfileGreen = createSwitchProfile(infraObj, switchProfileName1)
    switchProfileRed = createSwitchProfile(infraObj, switchProfileName2)

    #6.1 Add Leaf Selectors
    addLeafSelectorsVPC(switchProfileGreen, polIntName1, leafSelectorTo1, leafSelectorFrom1)
    addLeafSelectorsLeafAccessPort(switchProfileRed, polIntName2, leafSelectorTo2, leafSelectorFrom2)

    commit(switchProfileGreen, directoryObj)
    commit(switchProfileRed, directoryObj)


    #7.0 Create Bridge Domain
    bridgeDomain = createBridgeDomain(rootObj, tenantName, macAddr, bdName, ipAdd)
    commit(bridgeDomain, directoryObj)

    #8.0 Create Application Profile
    applicationProfile = createApplicationProfile(rootObj, infraObj, appName, tenantName, appDescr)
    commit(rootObj, directoryObj)

    #9.0 create EPGs
    epgGreen = createEPG(applicationProfile, nameEPG1)
    epgRed = createEPG(applicationProfile, nameEPG2)

    #9.1 add Domain
    addDomainToEPG(epgGreen, bdName, physDomName1)
    addDomainToEPG(epgRed, bdName, polIntName2)

    commit(applicationProfile, directoryObj)
    commit(epgRed, directoryObj)
    commit(epgGreen, directoryObj)

    #10.0 Map physical Ports
    mapPhysicalPortPolGroup(epgGreen, polName1)
    mapPhysicalPortPort(epgRed)

    commit(epgRed, directoryObj)
    commit(epgGreen, directoryObj)

    #11 Create Contract --> had a lot of issues implement contract with method so its hardcoded here
    fvTenant = cobra.model.fv.Tenant(rootObj, tenantName)

    vzBrCP = cobra.model.vz.BrCP(fvTenant, name=u'green_to_red', descr=u'', targetDscp=u'unspecified',
                                 prio=u'unspecified')
    vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', descr=u'', prio=u'unspecified', targetDscp=u'unspecified',
                                 consMatchT=u'AtleastOne', provMatchT=u'AtleastOne', name=u'Subject')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, action=u'permit', priorityOverride=u'default',
                                                   directives=u'', tnVzFilterName=u'default')

    # 11.1 provide Contract for Green
    fvRsProv = cobra.model.fv.RsProv(epgGreen, tnVzBrCPName=u'green_to_red')
    fvRsCons = cobra.model.fv.RsCons(epgGreen, tnVzBrCPName=u'DNS-NTP-ICMP')

    # 11.2 consume Contract for Red
    fvRsCons = cobra.model.fv.RsCons(epgRed, tnVzBrCPName=u'green_to_red')
    fvRsCons = cobra.model.fv.RsCons(epgRed, tnVzBrCPName=u'DNS-NTP-ICMP')

    commit(fvTenant, directoryObj)
    commit(epgRed, directoryObj)
    commit(epgGreen, directoryObj)

    #12 ADD DHCP to Bridge Domain
    addDHCP(bridgeDomain)

    commit(bridgeDomain, directoryObj)
    commit(rootObj, directoryObj)

    print('Script ENDED')

if __name__ == "__main__":
    main()
