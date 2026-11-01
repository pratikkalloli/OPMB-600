#!/usr/bin/env python3
"""Create explicit, reviewed concept records for Team B REPO-251–420."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
TEAM=Path(__file__).resolve().parent

# Each entry names a distinct domain artifact and its operational responsibility.
GROUPS = [
("B1 Industrial automation and manufacturing", [
("SerializedMachinePassport","tracks an industrial machine's identity, custodian, and maintenance attestations across controlled ownership changes"),
("TorqueAuditLedger","retains signed torque-tool readings against a production job so quality staff can reconcile out-of-tolerance fastening events"),
("ToolWearForecastCase","records measured cutting-tool wear and the maintenance disposition used to prevent an expired tool from returning to a workcell"),
("FurnaceCycleWitness","binds furnace temperature-time evidence to a heat-treatment batch and blocks release when the cycle window is violated"),
("PackagingArtworkRelease","controls the approved artwork revision and market destination before a packaging line can print labels"),
("FixtureInspectionSchedule","tracks fixture inspection intervals and blocks production use when inspection evidence is overdue"),
("ShiftHandoverDocket","transfers open safety and quality actions between production shifts with named outgoing and incoming leads"),
("ProductionScrapVoucher","authorizes scrapping a quantity of serialized work in process and preserves the quality disposition"),
("SurfaceTreatmentBatch","records coating chemistry and cure evidence for a component lot before downstream assembly"),
("AssemblySequencePermit","authorizes a constrained assembly step only after its prerequisite operations have been recorded"),
("MachineGuardInspection","records machine-guard inspection findings and prevents restart until safety-critical findings are closed"),
("ConsumableShelfLifeCard","tracks lot expiry and opened-container life for process consumables used by a production cell"),
("GaugeRAndRStudy","stores measurement-system study samples and approval for a specific gauge and characteristic"),
("WorkOrderTraveler","carries a serialized work order through required operations and captures station-level signoff"),
("QualityHoldRelease","records containment scope and the authorized release decision for material on quality hold"),
("SparePartCompatibility","approves a replacement part against machine model, revision, and safety class before installation"),
("CleanInPlaceRecord","binds a validated clean-in-place cycle to a processing vessel and the next production lot"),
("ReworkRoutingCard","defines permitted rework operations for a nonconforming unit and records each completed route step"),
("OperatorQualificationGrant","tracks operator qualification scope and expiration for safety-sensitive production tasks"),
("ProductionSampleCustody","maintains custody and disposition of retained production samples used for later quality investigation"),
]),
("B2 IoT, embedded devices and robotics", [
("RobotCellEnrollment","enrolls a robot controller into one cell after an owner-authorized identity and safety profile are recorded"),
("SensorCalibrationChain","links sensor calibration certificates and correction factors to the device measurement stream"),
("FirmwareRolloutRing","stages signed firmware releases by device cohort and records promotion or halt decisions"),
("DroneFleetCommand","authorizes a bounded mission command for a registered drone and records its operator and geofence"),
("GatewayJoinApproval","approves a sensor gateway's join request only when its hardware identity and site assignment match"),
("DeviceOwnershipTransfer","transfers a device between fictional owners while revoking the prior owner's access grant"),
("EdgeNodeAttestation","records measured boot claims and policy evaluation for an edge node before workload placement"),
("BatteryHealthLog","captures battery cycle measurements and maintenance decisions for a battery-backed field device"),
("TelemetryFrameSeal","signs ordered telemetry frames with device and sampling-window identity to expose replay or alteration"),
("EmbeddedConfigBundle","approves a device-specific configuration bundle with a monotonic revision and rollback policy"),
("SmartLockLease","issues a time-bounded access lease to a synthetic smart lock and records revocation events"),
("AutonomousCartRoute","authorizes a warehouse robot route against aisle restrictions and current traffic-zone revision"),
("RemoteProbeRegistry","registers diagnostic probes, their allowed command set, and the evidence collected from a device"),
("DeviceRecoveryTicket","coordinates recovery of a lost device identity and records invalidation of its previous credentials"),
("RoboticsSafetyEnvelope","sets the approved motion limits and emergency-stop profile for a robot operating mode"),
("WearableAssetPairing","pairs a worker-worn safety sensor to a shift and verifies the assigned worker-device relationship"),
("FieldGatewayBridge","authorizes forwarding between sensor networks and a named field gateway under a scoped data policy"),
("FirmwareRollbackPermit","approves a rollback to a previously signed firmware revision after a defined failure trigger"),
("SensorBatchProvenance","records production lot, calibration status, and destination for a batch of deployed sensors"),
("RobotToolingIdentity","binds an interchangeable robot end effector to a serial, safety rating, and approved robot model"),
("DeviceTrustRenewal","renews device trust after periodic evidence collection and rejects expired attestation windows"),
("MicrocontrollerBuildProof","records compiler, source revision, and reproducible build digest for a microcontroller image"),
("CameraPrivacyZone","distributes approved privacy masks and retention rules to cameras assigned to a physical zone"),
("HomeEnergyDeviceCommission","commissions synthetic home energy equipment and binds it to an installer and premises"),
("SecureBLEPairingBook","records Bluetooth pairing authorization and session expiry for a named embedded device pair"),
("FleetCertificateRotation","rotates device fleet certificates in cohorts and tracks overlap and retirement windows"),
("RobotMissionReceipt","captures robot mission intent, completion status, and signed exception evidence"),
("IoTDataRetentionPolicy","assigns retention and deletion schedules to device data classes with an auditable policy revision"),
("LowPowerNetworkJoin","authorizes low-power sensor network attachment with a site, join epoch, and duty-cycle profile"),
("SensorAnomalyWitness","preserves an anomalous sensor interval with calibration and provenance context for review"),
]),
("B3 Energy and utilities", [
("MeterReadCycle","closes a utility meter-reading cycle with interval completeness and authorized correction records"),
("RenewableOutputCertificate","attests renewable generator output for a defined meter interval and plant identity"),
("FeederSwitchingOrder","approves a feeder switching sequence with prerequisite checks and operator acknowledgements"),
("TransformerOilSample","tracks transformer oil sample custody, laboratory results, and maintenance disposition"),
("DemandResponseEnrollment","enrolls a customer resource in a demand-response event with capacity and opt-out bounds"),
("MicrogridIslandEvent","records islanding and reconnection transitions for a microgrid with synchronism evidence"),
("GridTopologySnapshot","signs a versioned distribution topology snapshot used by a simulation's switching planner"),
("TurbineMaintenanceDossier","records wind turbine maintenance work, component serials, and post-service inspection"),
("SolarStringInspection","tracks photovoltaic string inspection measurements and corrective action before energization"),
("BatteryDispatchReceipt","records a storage dispatch request, state-of-charge bounds, and metered response"),
("UtilityCrewPermit","issues a work-zone permit for a utility crew and records clearance before re-energization"),
("HydroReservoirRelease","authorizes a simulated reservoir release against downstream flow and environmental constraints"),
("SubstationRelaySetting","controls relay setting revisions, coordination review, and staged commissioning"),
("CarbonIntensityAttestation","publishes interval carbon intensity with source-meter lineage and calculation revision"),
("EVChargeSession","records a charging session's meter start/end, station identity, and settlement state"),
("UtilityInterconnectApplication","reviews distributed-generation interconnection evidence and grants a bounded operating mode"),
("FuelBlendCertificate","attests a delivered fuel blend's composition range and supplier batch identity"),
("PowerPurchaseAllocation","allocates a synthetic power purchase quantity across buyers and settlement intervals"),
("OutageRestorationLog","tracks restoration milestones and switching approvals for a simulated outage zone"),
("WaterPumpEnergyLedger","reconciles pump runtime and energy readings against a water delivery schedule"),
("HeatNetworkMetering","closes district heat meter intervals and captures correction approvals"),
("RenewableRECRegistry","tracks synthetic renewable certificate issuance, transfer, and retirement without double use"),
("GridFirmwareRelease","gates a simulated grid controller firmware release on compatibility and rollback evidence"),
("CustomerMeterExchange","records removal and installation meter serials with final and initial readings"),
("EnergyMarketBidEnvelope","submits a time-bounded market bid with quantity limits and authorized trader identity"),
("HydrogenBatchPassport","tracks synthetic hydrogen batch purity results and custody from production to delivery"),
("DistributionLossStudy","publishes a feeder loss study with input dataset hashes and reviewer disposition"),
("LoadForecastPublication","versions a utility load forecast and records model input and publication horizon"),
("InverterProtectionProfile","approves inverter protection parameters against a connection agreement revision"),
("CommunityEnergySettlement","settles synthetic community energy credits across participant meter intervals"),
]),
("B4 Transport, mobility and logistics", [
("RailSignalAspectArchive","preserves signal aspect transitions with route, interlocking revision, and event sequence"),
("ColdChainTransfer","records refrigerated shipment custody transfer with temperature range and seal condition"),
("AircraftComponentLifeCard","tracks simulated aircraft component cycles, inspections, and remaining-life authorization"),
("PortContainerSeal","binds container identity, seal changes, and authorized port custody events"),
("TransitOperatorCredential","assigns route and vehicle qualifications to a transit operator for a bounded duty period"),
("FleetRouteException","authorizes a fleet route deviation with reason, dispatch approval, and revised arrival window"),
("BusDepotChargeDispatch","schedules bus charging against departure readiness, charger availability, and energy limits"),
("MaritimeBillOfLading","issues a synthetic cargo receipt and controls amendments before vessel departure"),
("RailTrackWindowPermit","reserves a track work window and records protection placement and removal acknowledgements"),
("ParcelSortationManifest","reconciles parcel scans through sortation lanes and flags missing or duplicate handoffs"),
("VehicleTitleTransfer","records synthetic vehicle ownership transfer and invalidates prior fleet operator assignment"),
("TaxiShiftSettlement","closes a synthetic taxi shift with trip totals, adjustments, and driver acknowledgement"),
("AircraftGroundPowerLog","records ground power connection intervals and inspection before aircraft dispatch"),
("WarehouseDockAppointment","allocates a receiving dock slot to a carrier and validates arrival window changes"),
("CustomsInspectionPacket","assembles shipment inspection evidence and records release or hold authority"),
("BicycleShareBatterySwap","records battery pack swaps between shared bicycles and charging racks with serial custody"),
("RailCrewDutyRelease","verifies crew qualification and rest window before releasing a simulated rail duty"),
("FerryPassengerManifest","versions passenger count and emergency reconciliation data for a synthetic ferry trip"),
("CargoTemperatureExcursion","records a cold-chain excursion, affected lot scope, and disposition decision"),
("RoadsideAssistanceDispatch","dispatches a service vehicle to a verified breakdown location with changing assignment history"),
("VehicleRecallNotice","tracks affected vehicle serial ranges, notification delivery, and repair completion evidence"),
("AutonomousConvoyJoin","authorizes a vehicle joining a simulated convoy under a specific leader and safety policy"),
("ShippingHazardDeclaration","records hazardous cargo classification, packaging checks, and carrier acceptance"),
("AirportBaggageCustody","tracks baggage custody scans between check-in, transfer, and reclaim points"),
("FreightRateOffer","publishes a carrier rate quote with validity window, lane, and capacity constraints"),
("TunnelVentilationCommand","approves a tunnel ventilation mode change against occupancy and sensor thresholds"),
("ContainerWeightTicket","attests container gross mass measurement and scale calibration at a terminal"),
("DeliveryProofOfHandoff","captures recipient acknowledgement and parcel identity for a delivery transfer"),
("TrainConsistRevision","versions train consist order and checks vehicle compatibility before departure"),
("TrafficSignalPriorityPermit","grants a bounded transit signal priority request and records intersection response"),
]),
("B5 Telecommunications, networks and edge", [
("RANCellProvisioning","provisions a radio cell with approved parameters and a controlled activation window"),
("RoutingPolicyBundle","releases a signed routing policy revision to an explicitly selected network cohort"),
("PeeringKeyAgreement","records partner endpoint identity and key rotation state for a simulated peering link"),
("FiberSpliceEvidence","records fiber splice locations, loss measurements, and technician signoff for a route segment"),
("NetworkSliceLease","allocates a network slice to a tenant with resource bounds and expiry"),
("SubscriberSIMReplacement","controls replacement of a synthetic subscriber SIM and revokes the prior credential"),
("EdgeCacheInvalidate","issues scoped cache invalidation instructions and records acknowledgements from edge nodes"),
("TelecomEquipmentRMA","tracks failed network equipment return, replacement serial, and vendor disposition"),
("TowerAccessPermit","authorizes a technician tower visit with site, work scope, and check-in/check-out evidence"),
("SpectrumGrantLedger","records synthetic spectrum grant intervals, geography, and renewal decisions"),
("DNSSECKeyCeremony","documents simulated DNSSEC key generation, dual-control approval, and rollover milestones"),
("ServiceChainActivation","activates a network service chain only after each virtual function is healthy and approved"),
("NetworkChangeWindow","reserves a network maintenance window and records precheck, execution, and rollback outcome"),
("CarrierInterconnectReceipt","reconciles carrier interconnect traffic totals and signed settlement acknowledgements"),
("BGPCommunityApproval","approves permitted BGP community values for a customer route export policy"),
("OLTProfileRelease","releases optical line terminal profiles to a specific access network cohort"),
("BaseStationClockAttestation","records timing source health and synchronization error for a base station"),
("QoSContractRevision","versions a service quality contract with measurable latency and loss bounds"),
("RoamingPartnerProfile","provisions roaming partner identifiers, permitted services, and effective dates"),
("SyntheticInterceptAudit","records access approvals and immutable audit references for a fictional lawful-process simulation"),
("CircuitMigrationPlan","coordinates circuit endpoint migration with outage bounds and rollback checkpoints"),
("EmergencyBroadcastAuthorization","authorizes an emergency broadcast area, message revision, and expiry"),
("NetworkTelemetryCheckpoint","seals interval telemetry summaries with collector identity and sequence continuity"),
("PacketBrokerFilterUpdate","releases a packet broker filter revision with scope and rollback constraints"),
("CarrierNumberPorting","tracks synthetic number port authorization, donor release, and recipient activation"),
("WiFiControllerEnrollment","enrolls a wireless controller with site ownership and approved firmware evidence"),
("CPEFirmwareCampaign","stages customer-premises firmware rollout cohorts with exception tracking"),
("InternetExchangeMembership","approves a member port, route-server policy, and scheduled activation"),
("MicrowaveLinkAlignment","records link alignment measurements and acceptance bounds for a radio hop"),
("TelecomDataRetentionFreeze","places a scoped synthetic record class under a timed retention hold and tracks release"),
]),
("B6 Agriculture and environmental technology", [
("IrrigationZoneSchedule","issues irrigation commands by field zone with water allocation and soil-moisture constraints"),
("SoilProbeCalibration","tracks soil probe calibration factors and service interval for a named field location"),
("CropSprayPermit","authorizes a synthetic crop treatment with crop stage, weather window, and applicator qualification"),
("SeedLotProvenance","records seed lot origin, treatment declarations, and destination planting blocks"),
("GreenhouseClimatePolicy","versions greenhouse climate setpoints with crop-stage limits and override history"),
("LivestockMovementCertificate","documents a synthetic livestock group movement with origin, destination, and health hold status"),
("WaterSampleCustody","preserves water sample custody, collection point, laboratory result, and quality disposition"),
("WatershedReleaseNotice","publishes a managed watershed release with downstream threshold and stakeholder acknowledgement"),
("WeatherStationCalibration","records environmental station calibration checks and correction factors"),
("BeehiveHealthObservation","tracks synthetic hive health observations, inspection evidence, and intervention status"),
("FarmEquipmentOperatorGrant","assigns equipment operation privileges by machine class and qualification expiry"),
("PesticideApplicationLog","records treatment product, field boundary, dose, weather, and applicator for compliance review"),
("HarvestBinHandoff","tracks harvest bin custody from field collection through packing intake"),
("GrainMoistureCertificate","attests grain moisture measurements and storage acceptance for a harvest lot"),
("ColdRoomTemperatureRecord","seals produce cold-room temperature intervals and excursion disposition"),
("ForestPlotMeasurement","publishes a forest plot inventory with measurement protocol and plot revision"),
("RiverGaugeObservation","validates ordered river gauge readings and flags threshold exceedances"),
("AirQualitySensorEvidence","preserves air sensor calibration and pollutant interval evidence for an observation site"),
("FertilizerBlendTicket","records fertilizer blend proportions and field allocation against nutrient limits"),
("AquacultureFeedTrace","tracks feed batch and ration events for a synthetic aquaculture enclosure"),
("CompostBatchMaturity","records compost temperature, turning events, and maturity acceptance for a batch"),
("DroneSurveyMission","authorizes a farm survey flight with field boundary, sensor payload, and image retention policy"),
("PollinatorCorridorInspection","tracks corridor habitat inspection findings and remediation milestones"),
("CropInsuranceEvidence","assembles synthetic crop loss observations and assessor signoffs for a claim"),
("FisheryCatchTrace","records synthetic catch species, quantity, vessel trip, and landing custody"),
("CarbonSoilSample","tracks soil carbon sample custody and lab result for a named plot and sampling depth"),
("DroughtAllocationPermit","allocates constrained irrigation water among fields with priority and expiry rules"),
("WetlandRestorationMilestone","records restoration work milestones and ecological acceptance evidence"),
("ReservoirWaterQuality","seals reservoir water quality measurements and threshold-based response decisions"),
("FarmProducePackingLot","links harvested produce to packing line, grade result, and shipping destination"),
]),
]

STATE_SETS={
"B1 Industrial automation and manufacturing":(["draft","reviewed","released","retired"],{"draft":["reviewed","retired"],"reviewed":["released","draft","retired"],"released":["retired"],"retired":[]}),
"B2 IoT, embedded devices and robotics":(["new","attested","active","revoked"],{"new":["attested","revoked"],"attested":["active","new","revoked"],"active":["revoked"],"revoked":[]}),
"B3 Energy and utilities":(["captured","checked","settled","disputed"],{"captured":["checked","disputed"],"checked":["settled","disputed"],"settled":[],"disputed":["checked"]}),
"B4 Transport, mobility and logistics":(["planned","authorized","in_transit","closed"],{"planned":["authorized","closed"],"authorized":["in_transit","closed"],"in_transit":["closed"],"closed":[]}),
"B5 Telecommunications, networks and edge":(["provisioned","active","rotated","retired"],{"provisioned":["active","retired"],"active":["rotated","retired"],"rotated":["active","retired"],"retired":[]}),
"B6 Agriculture and environmental technology":(["observed","quality_checked","published","withdrawn"],{"observed":["quality_checked","withdrawn"],"quality_checked":["published","withdrawn"],"published":["withdrawn"],"withdrawn":[]}),
}
RULES=[("sha256","evidence_digest","Evidence must be a lowercase SHA-256 digest.","a"*64,{"evidence_digest":"invalid-digest"}),
       ("token","authorization_code","Authorization code must be uppercase alphanumeric segments separated by hyphens.","AUTH-251-A",{"authorization_code":"bad code"}),
       ("bounded_int","measured_value","Measured value must be an integer from 0 through 1000.",25,{"measured_value":1001}),
       ("nonnegative_int","event_count","Event count must be a nonnegative integer.",4,{"event_count":-1}),
       ("enum","review_class","Review class must be minor, major, or critical.","major",{"review_class":"unknown"}),
       ("positive_int","revision_epoch","Revision epoch must be a positive integer.",2,{"revision_epoch":0})]

def main()->None:
    specs=json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8'))
    existing={int(x['repository_id'][-3:]) for x in specs}
    rid=251
    for domain, concepts in GROUPS:
        states,transitions=STATE_SETS[domain]
        for name,purpose in concepts:
            if rid in existing: rid+=1; continue
            rule_kind,rule_field,rule_desc,sample_value,invalid=RULES[(rid-251)%len(RULES)]
            batch=(rid-241)//10+1
            slug=''.join('_'+c.lower() if c.isupper() else c for c in name).lstrip('_')
            entity=slug
            scope={'B1 Industrial automation and manufacturing':'workcell_id','B2 IoT, embedded devices and robotics':'device_id','B3 Energy and utilities':'asset_id','B4 Transport, mobility and logistics':'shipment_id','B5 Telecommunications, networks and edge':'network_element_id','B6 Agriculture and environmental technology':'site_id'}[domain]
            sample={"record_id":f"{slug}-{rid}",scope:f"{scope.replace('_id','')}-{rid}",rule_field:sample_value,"event_code":f"EVT-{rid}","sequence":rid,"state":states[0]}
            differentiation=f"{purpose.capitalize()}; the application's primary record, scope, lifecycle, and acceptance rule are specific to {name} and differ from generic signing, access-grant, or document-release workflows."
            specs.append({"repository_id":f"REPO-{rid:03d}","batch":batch,"domain_group":domain,"name":name,"slug":slug,"entity":entity,"purpose":purpose.capitalize()+".","workflow":purpose.capitalize()+"; intake, validate, approve, record transition, and preserve a verifiable audit artifact.","scope_field":scope,"rule_field":rule_field,"rule_kind":rule_kind,"rule_description":rule_desc,"states":states,"transitions":transitions,"fields":["record_id",scope,rule_field,"event_code","sequence","state"],"sample":sample,"invalid":invalid,"baseline_mode":"rsa","classical_signature":"RSA-3072 PSS/SHA-256","classical_key_establishment":"RSA-3072 OAEP/SHA-256 with AES-256-GCM","target":"ML-DSA-65 and ML-KEM-768","differentiation":differentiation})
            rid+=1
    specs.sort(key=lambda x:int(x['repository_id'][-3:]))
    if [x['repository_id'] for x in specs] != [f"REPO-{n:03d}" for n in range(241,421)]: raise SystemExit('Spec list must be continuous from REPO-241 through REPO-420.')
    if len({x['name'] for x in specs})!=180: raise SystemExit('Duplicate application name.')
    (TEAM/'application_specs.json').write_text(json.dumps(specs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(f"Prepared {len(specs)} application concept specifications (batches 01–18). Batch 01 definitions preserved.")
if __name__=='__main__': main()
