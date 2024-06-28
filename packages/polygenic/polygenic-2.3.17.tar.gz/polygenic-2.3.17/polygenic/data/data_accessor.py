import logging
from polygenic.data.vcf_accessor import VcfAccessor
from polygenic.data.vcf_record import VcfRecord

logger = logging.getLogger('description_language.' + __name__)

class DataAccessor(object):
    def __init__(self, 
        genotypes: VcfAccessor,
        allele_frequencies: VcfAccessor = None,
        sample_name: str = None,
        model_name: str = "",
        af_field_name: str = "AF_nfe",
        parameters = {}):
        self.__genotypes = genotypes
        self.__allele_frequencies = allele_frequencies
        if sample_name is None:
            sample_name = genotypes.get_sample_names()[0]
        self.__sample_name = sample_name
        self.__af_field_name = af_field_name
        self.__parameters = parameters
        self.__cache = {}

    def get_parameters(self) -> dict:
        return(self.__parameters)

    def get_genotype_by_rsid(self, rsid) -> VcfRecord:
        if rsid in self.__cache:
            return self.__cache[rsid]
        genotype = {"rsid": rsid}
        if not self.__genotypes is None:
            record = self.__genotypes.get_record_by_rsid(rsid)
            #print("====================>" + str(rsid) + " " + " " + str(record.get_ref()))
            if not record is None:
                genotype["genotype"] = record.get_genotype(self.__sample_name)
                genotype["phased"] = record.is_phased(self.__sample_name)
                if genotype["genotype"][0] is None:
                    if not self.__allele_frequencies is None:
                        af_record = self.__allele_frequencies.get_record_by_rsid(rsid)
                        if af_record is not None:
                            genotype["genotype"] = af_record.get_genotype_by_af(self.__af_field_name)
                            genotype["phased"] = False
                            genotype["source"] = "af"
                            genotype["ref"] = af_record.get_ref()
                            self.__cache[rsid] = genotype
                            return genotype
                    if record.get_ref() is not None:
                        genotype["genotype"] = [record.get_ref(), record.get_ref()]
                        genotype["phased"] = False
                        genotype["source"] = "reference"
                        genotype["ref"] = record.get_ref()
                        self.__cache[rsid] = genotype
                        return genotype
                    record is None
                else:
                    if record.is_ldproxy(self.__sample_name):
                        genotype["source"] = "ldproxy"
                    elif record.is_imputed():
                        genotype["source"] = "imputing"
                    else:   
                        genotype["source"] = "genotyping"
                    genotype["ref"] = record.get_ref()
                    self.__cache[rsid] = genotype
                    return genotype
        genotype["genotype"] = [None, None]
        genotype["phased"] = None
        genotype["source"] = "missing"
        genotype["ref"] = None
        self.__cache[rsid] = genotype
        return genotype

            

