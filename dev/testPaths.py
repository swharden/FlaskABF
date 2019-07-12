folders = R"""
X:\Data\SD\LHA Oxytocin\pilot study
X:\Data
X:\Data\OT-Cre\OT-GCaMP-nonspecific
X:\Data\AT1-Cre\SFO Chr2 PVN
X:\Data\AT1-Cre\MPO Chr2 PVN
X:\Data\AT1-Cre\global Chr2 NTS\data
X:\Data\AT1-Cre\MPO Chr2 PVN
X:\Data\OTR-Cre\PFC inj CHR2 BLA phenotype
X:\Data\OTR-Cre\PFC inj CHR2 PFC IPSCs
X:\Data\OTR-Cre\PFC inj CHR2 PFC EPSCs
X:\Data\OTR-Cre\PFC inj eYFP OXT response
X:\Data\F344\Aging BLA\basal excitability round1
X:\Data\F344\Aging BLA\basal excitability round2
X:\Data\F344\Aging BLA\basal excitability round3
X:\Data\F344\Aging BLA\halo\data
X:\Data\F344\Aging Hipp\AMPA-NMDA-Ratio
X:\Data\F344\Aging Hipp\E-I-balance
X:\Data\TH-Cre (rat)
X:\Data\OT-Cre\calcium-mannitol
X:\Data\OT-Cre\BNST-CeA pathway
X:\Data\SD\Piriform Oxytocin
X:\Data\CRH-Cre\oxt-tone\injection-gain-analysis-2
X:\Data\CRH-Cre\oxt-tone\OXT-on-CRH-neurons
X:\Data\CRH-Cre\oxt-tone\OXT-preincubation
X:\Data\CRH-Cre\oxt-tone\Salt loading TGOT 50nm
X:\Data\CRH-Cre\oxt-tone\OXT-preincubation
X:\Data\AT1-Cre\MPO Chr2 PVN
X:\Data\AT1-Cre\MPO Chr2 PVN\abfs
X:\Data\C57\OVLT angiotensin
X:\Data\C57\Tat project
X:\Data\winstar\D2R NAc halo
X:\Data\OT-Cre\microsphere testing\PFC injection
X:\Data\C57\dreadd experiments
""".split("\n")
folders = [x.strip() for x in folders]
folders = [x for x in folders if len(x)]

abfs = R"""
X:\Data\CRH-Cre\oxt-tone\OXT-preincubation\19709_sh_0015
X:\Data\AT1-Cre\global Chr2 NTS\data\17n14012
X:\Data\SD\LHA Oxytocin\pilot study\abfs\17608012
X:\Data\SD\LHA Oxytocin\pilot study\abfs\17601000
""".split("\n")
abfs = [x.strip() for x in abfs]
abfs = [x for x in abfs if len(x)]