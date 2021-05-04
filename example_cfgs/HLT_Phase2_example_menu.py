
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process("MYHLT", eras.Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input  = cms.untracked.int32(100),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(''),
    secondaryFileNames = cms.untracked.vstring()
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

# -- L1 emulation -- #
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.L1TkMuons.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")
process.L1TkMuons.applyQualityCuts = cms.bool(True)
# -- #

# -- HLTriggerFinalPath -- #
process.hltTriggerSummaryAOD = cms.EDProducer( "TriggerSummaryProducerAOD",
    moduleLabelPatternsToSkip = cms.vstring(  ),
    processName = cms.string( "@" ),
    moduleLabelPatternsToMatch = cms.vstring( 'hlt*', 'L1Tk*' ),
    throw = cms.bool( False )
)
process.hltTriggerSummaryRAW = cms.EDProducer( "TriggerSummaryProducerRAW",
    processName = cms.string( "@" )
)
process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( False )
)
process.HLTriggerFinalPath = cms.Path(
    process.hltTriggerSummaryAOD+
    process.hltTriggerSummaryRAW+
    process.hltBoolFalse
)
# -- #

# -- HLT paths -- #
from HLTrigger.PhaseII.Muon.Customizers.loadPhase2MuonHLTPaths_cfi import loadPhase2MuonHLTPaths
process = loadPhase2MuonHLTPaths(process)

process.schedule = cms.Schedule(
    process.L1simulation_step,
    process.L1_SingleTkMuon_22,
    process.L1_DoubleTkMuon_15_7,
    process.L1_TripleTkMuon_5_3_3,
    process.HLT_Mu50_FromL1TkMuon_Open,
    process.HLT_Mu50_FromL1TkMuon,
    process.HLT_IsoMu24_FromL1TkMuon,
    process.HLT_Mu37_Mu27_FromL1TkMuon,
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,
    process.HLTriggerFinalPath
)
# -- #

# -- Test Setup -- #
process.load( "DQMServices.Core.DQMStore_cfi" )
process.DQMStore.enableMultiThread = True

process.GlobalTag.globaltag = "111X_mcRun4_realistic_T15_v3"

process.source.fileNames = cms.untracked.vstring(
    "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FC1C5501-17FF-AD4E-B0C2-78B114D94AD6.root",
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 100 )
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool( True ),
    numberOfThreads = cms.untracked.uint32( 1 ),
    numberOfStreams = cms.untracked.uint32( 0 ),
    sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
)

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('L1TGlobalSummary')
    process.MessageLogger.categories.append('HLTrigReport')
    process.MessageLogger.categories.append('FastReport')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1  # 1000
# -- #


from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000
process = customise_aging_1000(process)

from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

from HLTrigger.Configuration.Eras import modifyHLTforEras
modifyHLTforEras(process)


# process.Timing = cms.Service("Timing",
#     summaryOnly = cms.untracked.bool(True),
#     useJobReport = cms.untracked.bool(True)
# )

# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#     ignoreTotal = cms.untracked.int32(1)
# )

# print process.dumpPython()

