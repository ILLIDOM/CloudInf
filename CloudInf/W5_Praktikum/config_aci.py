import cobra.mit.request
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
import urllib3.contrib.pyopenssl
from cobra.model import pol, phys, infra, fvns, aaa, fv, vz, dhcp

# is needed; else a ssl error occurs
urllib3.disable_warnings()

# informations to connect to apic
apicURL = 'https://10.18.1.10/'
userName = 'group10'
password = '0d3t0UrPLo8X'

# login to APIC and create directory Object
loginSession = LoginSession(apicURL, userName, password)
moDir = MoDirectory(loginSession)
moDir.login()

# creating top level object on which operations will be made
polUni = cobra.model.pol.Uni('')
infraInfra = cobra.model.infra.Infra(polUni)
infraFuncP = cobra.model.infra.FuncP(infraInfra)

#1 creating VLANPools --->    und encap block mitgeben
#1.1 Server Green
vlanServerGreen = cobra.model.fvns.VlanInstP(infraInfra,
                                             ownerKey='',
                                             name='Group10-VLAN510',
                                             descr='VLAN Pool for Server Green',
                                             allocMode='static')

#EncapBlock
fvnsVlanInstPGreen = cobra.model.fvns.VlanInstP(infraInfra, 'Group10-VLAN510', 'static')
fvnsEncapBlkGreen = cobra.model.fvns.EncapBlk(fvnsVlanInstPGreen, from_=u'vlan-510', to=u'vlan-510', allocMode=u'static')

#1.2 Server Red
vlanServerRed = cobra.model.fvns.VlanInstP(infraInfra,
                                             ownerKey='',
                                             name='Group10-VLAN710',
                                             descr='VLAN Pool for Server Red',
                                             nameAlias='',
                                             ownerTag='',
                                             annotation='',
                                             allocMode='static')
#EncapBlock
fvnsVlanInstPRed = cobra.model.fvns.VlanInstP(infraInfra, 'Group10-VLAN710', 'static')
fvnsEncapBlkRed = cobra.model.fvns.EncapBlk(fvnsVlanInstPRed, from_=u'vlan-710', to=u'vlan-710', allocMode=u'static')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(infraInfra)
modification.addMo(fvnsVlanInstPGreen)
modification.addMo(fvnsVlanInstPRed)
moDir.commit(modification)

#2 Create physical Domains per server

#2.1 Server Green
physDomPGreen = cobra.model.phys.DomP(polUni, name=u'Group10-DOMAIN-GREEN')
aaaDomainRefGreen = cobra.model.aaa.DomainRef(physDomPGreen, name=u'group10')
infraRsVlanNsGreen = cobra.model.infra.RsVlanNs(physDomPGreen, tDn=u'uni/infra/vlanns-[Group10-VLAN510]-static')


#2.2 Server Red
physDomPRed = cobra.model.phys.DomP(polUni, name=u'Group10-DOMAIN-RED')
aaaDomainRefRed = cobra.model.aaa.DomainRef(physDomPRed, name=u'group10')
infraRsVlanNsRed = cobra.model.infra.RsVlanNs(physDomPRed, tDn=u'uni/infra/vlanns-[Group10-VLAN710]-static')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(polUni)
moDir.commit(modification)

#3 create AAEP
#3.1 Server Green
infraAttEntityPGreen = cobra.model.infra.AttEntityP(infraInfra, name=u'Group10-AAEP-GREEN', descr=u'AAEP for server green')
infraRsDomPGreen = cobra.model.infra.RsDomP(infraAttEntityPGreen, tDn=u'uni/phys-Group10-DOMAIN-GREEN')

#3.2 Server Red
infraAttEntityPRed = cobra.model.infra.AttEntityP(infraInfra, name=u'Group10-AAEP-RED', descr=u'AAEP for server red')
infraRsDomPRed = cobra.model.infra.RsDomP(infraAttEntityPRed, tDn=u'uni/phys-Group10-DOMAIN-RED')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(infraInfra)
moDir.commit(modification)


#4 create Policy Groups
#4.1 Server Green -> VPC Interface
infraAccBndlGrp = cobra.model.infra.AccBndlGrp(infraFuncP, name=u'Group10-POLGROUP-GREEN', descr=u'POLGROUP for Server Green', lagT=u'node')
infraRsLacpPol = cobra.model.infra.RsLacpPol(infraAccBndlGrp, tnLacpLagPolName=u'LACP')
infraRsCdpIfPolGreen = cobra.model.infra.RsCdpIfPol(infraAccBndlGrp, tnCdpIfPolName=u'CDP_ON')
infraRsAttEntPGreen = cobra.model.infra.RsAttEntP(infraAccBndlGrp, tDn=u'uni/infra/attentp-Group10-AAEP-GREEN')


#4.2 Server Red -> Leaf Access Port
infraAccPortGrp = cobra.model.infra.AccPortGrp(infraFuncP, name=u'Group10-POLGROUP-RED', descr=u'POLGROUP for Server Red')
infraRsCdpIfPolRed = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=u'CDP_ON')
infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=u'LLDP_ON')
infraRsAttEntPRed = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=u'uni/infra/attentp-Group10-AAEP-RED')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(infraFuncP)
moDir.commit(modification)

#5 create Port Interface Profiles and assign Port to Interface
#5.1 Server Green
infraAccPortPGreen = cobra.model.infra.AccPortP(infraInfra,
                                                name=u'Group10-INTPROFILE-GREEN',
                                                descr=u'Interface Profile for Server Green')

infraHPortSGreen = cobra.model.infra.HPortS(infraAccPortPGreen, ownerKey=u'', name=u'e1-14', descr=u'', nameAlias=u'', ownerTag=u'', type=u'range', annotation=u'')
infraPortBlkGreen = cobra.model.infra.PortBlk(infraHPortSGreen, name=u'block2', fromPort=u'14', toPort=u'14')
infraRsAccBaseGrpGreen = cobra.model.infra.RsAccBaseGrp(infraHPortSGreen, tDn=u'uni/infra/funcprof/accbundle-Group10-POLGROUP-GREEN')


#5.2 Server Red --> POLGROUP zuweisen
infraAccPortPRed = cobra.model.infra.AccPortP(infraInfra,
                                                name=u'Group10-INTPROFILE-RED',
                                                descr=u'Interface Profile for Server Red')

infraHPortSRed = cobra.model.infra.HPortS(infraAccPortPRed, ownerKey=u'', name=u'e1-29', descr=u'', nameAlias=u'', ownerTag=u'', type=u'range', annotation=u'')
infraPortBlkRed = cobra.model.infra.PortBlk(infraHPortSRed, name=u'block2', fromPort=u'29', toPort=u'29')
infraRsAccBaseGrpRed = cobra.model.infra.RsAccBaseGrp(infraHPortSRed, tDn=u'uni/infra/funcprof/accportgrp-Group10-POLGROUP-RED')


# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(infraInfra)
modification.addMo(infraAccPortPGreen)
modification.addMo(infraAccPortPRed)
moDir.commit(modification)

#6 create Switch Profiles and add Leaf Selectors
#6.1 Server Green
infraNodePGreen = cobra.model.infra.NodeP(infraInfra, name=u'Group10-Leaf1-Leaf2')
infraRsAccPortPGreen = cobra.model.infra.RsAccPortP(infraNodePGreen, tDn=u'uni/infra/accportprof-Group10-INTPROFILE-GREEN')
infraLeafSGreen = cobra.model.infra.LeafS(infraNodePGreen, type=u'range', name=u'VPC')
infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafSGreen, to_=u'102', from_=u'101', name=u'2314c722b8025597')


#6.2 Server Red
infraNodePRed = cobra.model.infra.NodeP(infraInfra, name=u'Group10-Leaf2')
infraRsAccPortPRed = cobra.model.infra.RsAccPortP(infraNodePRed, tDn=u'uni/infra/accportprof-Group10-INTPROFILE-RED')
infraLeafSRed = cobra.model.infra.LeafS(infraNodePRed, type=u'range', name=u'LeafAccessPort')
infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafSRed, to_=u'102', from_=u'102', name=u'2d3e0d4a8657de19')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(infraNodePGreen)
modification.addMo(infraNodePRed)
moDir.commit(modification)

#7 create Bridge Domain
fvTenant = cobra.model.fv.Tenant(polUni, 'group10')
fvBD = cobra.model.fv.BD(fvTenant, mac=u'00:22:BD:F8:19:FF', name=u'green-red_BD')
fvSubnet = cobra.model.fv.Subnet(fvBD, ip=u'192.168.10.1/24', ctrl=u'unspecified')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=u'default')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(fvTenant)
moDir.commit(modification)

#8 create Application Profile
infraFuncP = cobra.model.infra.FuncP(infraInfra)
infraAccPortGrp = cobra.model.infra.AccPortGrp(infraFuncP,name=u'ApplicationProfile', descr=u'Application Profile Group10')
infraRsL2PortAuthPol = cobra.model.infra.RsL2PortAuthPol(infraAccPortGrp)
fvTenant = cobra.model.fv.Tenant(polUni, 'group10')
fvAp = cobra.model.fv.Ap(fvTenant, name=u'green-red')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(polUni)
moDir.commit(modification)

#9 create EPGs and add Domain
#9.1 green
fvAEPgGreen = cobra.model.fv.AEPg(fvAp, name=u'green_EPG')
fvRsBd = cobra.model.fv.RsBd(fvAEPgGreen, tnFvBDName=u'green-red_BD')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPgGreen, tDn=u'uni/phys-Group10-DOMAIN-GREEN', resImedcy=u'immediate')


#9.2 red
fvAEPgRed = cobra.model.fv.AEPg(fvAp, name=u'red_EPG')
fvRsBd = cobra.model.fv.RsBd(fvAEPgRed, tnFvBDName=u'green-red_BD')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPgRed, tDn=u'uni/phys-Group10-DOMAIN-RED', resImedcy=u'immediate')


modification = cobra.mit.request.ConfigRequest()
modification.addMo(fvAp)
modification.addMo(fvAEPgGreen)
modification.addMo(fvAEPgRed)
moDir.commit(modification)


#10 Map physical Ports
#10.1 server green

fvRsPathAtt = cobra.model.fv.RsPathAtt(fvAEPgGreen,
                                       tDn=u'topology/pod-1/protpaths-101-102/pathep-[Group10-POLGROUP-GREEN]',
                                       encap=u'vlan-510')


#10.2 server red
fvRsPathAtt = cobra.model.fv.RsPathAtt(fvAEPgRed,
                                       tDn=u'topology/pod-1/paths-102/pathep-[eth1/29]',
                                       encap=u'vlan-710')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(fvAEPgGreen)
modification.addMo(fvAEPgRed)
moDir.commit(modification)


#11 Create Contract
vzBrCP = cobra.model.vz.BrCP(fvTenant, ownerKey=u'', name=u'green_to_red', descr=u'', targetDscp=u'unspecified', nameAlias=u'', ownerTag=u'', prio=u'unspecified', annotation=u'')
vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', descr=u'', prio=u'unspecified', targetDscp=u'unspecified', nameAlias=u'', consMatchT=u'AtleastOne', annotation=u'', provMatchT=u'AtleastOne', name=u'Subject')
vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, action=u'permit', priorityOverride=u'default', directives=u'', annotation=u'', tnVzFilterName=u'default')

#11.1 provide Contract for Green
fvRsProv = cobra.model.fv.RsProv(fvAEPgGreen, tnVzBrCPName=u'green_to_red')
fvRsCons = cobra.model.fv.RsCons(fvAEPgGreen, tnVzBrCPName=u'DNS-NTP-ICMP')


#11.2 consume Contract for Red
fvRsCons = cobra.model.fv.RsCons(fvAEPgRed, tnVzBrCPName=u'green_to_red')
fvRsCons = cobra.model.fv.RsCons(fvAEPgRed, tnVzBrCPName=u'DNS-NTP-ICMP')

#commit
modification = cobra.mit.request.ConfigRequest()
modification.addMo(fvTenant)
modification.addMo(fvAEPgGreen)
modification.addMo(fvAEPgRed)
moDir.commit(modification)

#add DHCP to Bridge Domain
dhcpLbl = cobra.model.dhcp.Lbl(fvBD, name=u'Blue-DHCP')

# commit the generated code to APIC
modification = cobra.mit.request.ConfigRequest()
modification.addMo(fvBD)
modification.addMo(polUni)
moDir.commit(modification)

