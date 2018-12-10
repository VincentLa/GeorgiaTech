drop table if exists model_demog_dx;
create table model_demog_dx as
select
  model_demog.hadm_id,
  model_demog.hospital_expire_flag,
  model_demog.is_male,
  model_demog.age_at_admit,
  model_demog.admission_type,
  model_demog.insurance,
  model_demog.language,
  model_demog.marital_status,
  model_demog.ethnicity,
  coalesce(adm.ccs_0, 0) as ccs_0,
  coalesce(adm.ccs_1, 0) as ccs_1,
  coalesce(adm.ccs_2, 0) as ccs_2,
  coalesce(adm.ccs_3, 0) as ccs_3,
  coalesce(adm.ccs_4, 0) as ccs_4,
  coalesce(adm.ccs_5, 0) as ccs_5,
  coalesce(adm.ccs_6, 0) as ccs_6,
  coalesce(adm.ccs_7, 0) as ccs_7,
  coalesce(adm.ccs_8, 0) as ccs_8,
  coalesce(adm.ccs_9, 0) as ccs_9,
  coalesce(adm.ccs_10, 0) as ccs_10,
  coalesce(adm.ccs_11, 0) as ccs_11,
  coalesce(adm.ccs_12, 0) as ccs_12,
  coalesce(adm.ccs_13, 0) as ccs_13,
  coalesce(adm.ccs_14, 0) as ccs_14,
  coalesce(adm.ccs_15, 0) as ccs_15,
  coalesce(adm.ccs_16, 0) as ccs_16,
  coalesce(adm.ccs_17, 0) as ccs_17,
  coalesce(adm.ccs_18, 0) as ccs_18,
  coalesce(adm.ccs_19, 0) as ccs_19,
  coalesce(adm.ccs_20, 0) as ccs_20,
  coalesce(adm.ccs_21, 0) as ccs_21,
  coalesce(adm.ccs_22, 0) as ccs_22,
  coalesce(adm.ccs_23, 0) as ccs_23,
  coalesce(adm.ccs_24, 0) as ccs_24,
  coalesce(adm.ccs_25, 0) as ccs_25,
  coalesce(adm.ccs_26, 0) as ccs_26,
  coalesce(adm.ccs_27, 0) as ccs_27,
  coalesce(adm.ccs_28, 0) as ccs_28,
  coalesce(adm.ccs_29, 0) as ccs_29,
  coalesce(adm.ccs_30, 0) as ccs_30,
  coalesce(adm.ccs_31, 0) as ccs_31,
  coalesce(adm.ccs_32, 0) as ccs_32,
  coalesce(adm.ccs_33, 0) as ccs_33,
  coalesce(adm.ccs_34, 0) as ccs_34,
  coalesce(adm.ccs_35, 0) as ccs_35,
  coalesce(adm.ccs_36, 0) as ccs_36,
  coalesce(adm.ccs_37, 0) as ccs_37,
  coalesce(adm.ccs_38, 0) as ccs_38,
  coalesce(adm.ccs_39, 0) as ccs_39,
  coalesce(adm.ccs_40, 0) as ccs_40,
  coalesce(adm.ccs_41, 0) as ccs_41,
  coalesce(adm.ccs_42, 0) as ccs_42,
  coalesce(adm.ccs_43, 0) as ccs_43,
  coalesce(adm.ccs_44, 0) as ccs_44,
  coalesce(adm.ccs_45, 0) as ccs_45,
  coalesce(adm.ccs_46, 0) as ccs_46,
  coalesce(adm.ccs_47, 0) as ccs_47,
  coalesce(adm.ccs_48, 0) as ccs_48,
  coalesce(adm.ccs_49, 0) as ccs_49,
  coalesce(adm.ccs_50, 0) as ccs_50,
  coalesce(adm.ccs_51, 0) as ccs_51,
  coalesce(adm.ccs_52, 0) as ccs_52,
  coalesce(adm.ccs_53, 0) as ccs_53,
  coalesce(adm.ccs_54, 0) as ccs_54,
  coalesce(adm.ccs_55, 0) as ccs_55,
  coalesce(adm.ccs_56, 0) as ccs_56,
  coalesce(adm.ccs_57, 0) as ccs_57,
  coalesce(adm.ccs_58, 0) as ccs_58,
  coalesce(adm.ccs_59, 0) as ccs_59,
  coalesce(adm.ccs_60, 0) as ccs_60,
  coalesce(adm.ccs_61, 0) as ccs_61,
  coalesce(adm.ccs_62, 0) as ccs_62,
  coalesce(adm.ccs_63, 0) as ccs_63,
  coalesce(adm.ccs_64, 0) as ccs_64,
  coalesce(adm.ccs_65, 0) as ccs_65,
  coalesce(adm.ccs_66, 0) as ccs_66,
  coalesce(adm.ccs_67, 0) as ccs_67,
  coalesce(adm.ccs_68, 0) as ccs_68,
  coalesce(adm.ccs_69, 0) as ccs_69,
  coalesce(adm.ccs_70, 0) as ccs_70,
  coalesce(adm.ccs_71, 0) as ccs_71,
  coalesce(adm.ccs_72, 0) as ccs_72,
  coalesce(adm.ccs_73, 0) as ccs_73,
  coalesce(adm.ccs_74, 0) as ccs_74,
  coalesce(adm.ccs_75, 0) as ccs_75,
  coalesce(adm.ccs_76, 0) as ccs_76,
  coalesce(adm.ccs_77, 0) as ccs_77,
  coalesce(adm.ccs_78, 0) as ccs_78,
  coalesce(adm.ccs_79, 0) as ccs_79,
  coalesce(adm.ccs_80, 0) as ccs_80,
  coalesce(adm.ccs_81, 0) as ccs_81,
  coalesce(adm.ccs_82, 0) as ccs_82,
  coalesce(adm.ccs_83, 0) as ccs_83,
  coalesce(adm.ccs_84, 0) as ccs_84,
  coalesce(adm.ccs_85, 0) as ccs_85,
  coalesce(adm.ccs_86, 0) as ccs_86,
  coalesce(adm.ccs_87, 0) as ccs_87,
  coalesce(adm.ccs_88, 0) as ccs_88,
  coalesce(adm.ccs_89, 0) as ccs_89,
  coalesce(adm.ccs_90, 0) as ccs_90,
  coalesce(adm.ccs_91, 0) as ccs_91,
  coalesce(adm.ccs_92, 0) as ccs_92,
  coalesce(adm.ccs_93, 0) as ccs_93,
  coalesce(adm.ccs_94, 0) as ccs_94,
  coalesce(adm.ccs_95, 0) as ccs_95,
  coalesce(adm.ccs_96, 0) as ccs_96,
  coalesce(adm.ccs_97, 0) as ccs_97,
  coalesce(adm.ccs_98, 0) as ccs_98,
  coalesce(adm.ccs_99, 0) as ccs_99,
  coalesce(adm.ccs_100, 0) as ccs_100,
  coalesce(adm.ccs_101, 0) as ccs_101,
  coalesce(adm.ccs_102, 0) as ccs_102,
  coalesce(adm.ccs_103, 0) as ccs_103,
  coalesce(adm.ccs_104, 0) as ccs_104,
  coalesce(adm.ccs_105, 0) as ccs_105,
  coalesce(adm.ccs_106, 0) as ccs_106,
  coalesce(adm.ccs_107, 0) as ccs_107,
  coalesce(adm.ccs_108, 0) as ccs_108,
  coalesce(adm.ccs_109, 0) as ccs_109,
  coalesce(adm.ccs_110, 0) as ccs_110,
  coalesce(adm.ccs_111, 0) as ccs_111,
  coalesce(adm.ccs_112, 0) as ccs_112,
  coalesce(adm.ccs_113, 0) as ccs_113,
  coalesce(adm.ccs_114, 0) as ccs_114,
  coalesce(adm.ccs_115, 0) as ccs_115,
  coalesce(adm.ccs_116, 0) as ccs_116,
  coalesce(adm.ccs_117, 0) as ccs_117,
  coalesce(adm.ccs_118, 0) as ccs_118,
  coalesce(adm.ccs_119, 0) as ccs_119,
  coalesce(adm.ccs_120, 0) as ccs_120,
  coalesce(adm.ccs_121, 0) as ccs_121,
  coalesce(adm.ccs_122, 0) as ccs_122,
  coalesce(adm.ccs_123, 0) as ccs_123,
  coalesce(adm.ccs_124, 0) as ccs_124,
  coalesce(adm.ccs_125, 0) as ccs_125,
  coalesce(adm.ccs_126, 0) as ccs_126,
  coalesce(adm.ccs_127, 0) as ccs_127,
  coalesce(adm.ccs_128, 0) as ccs_128,
  coalesce(adm.ccs_129, 0) as ccs_129,
  coalesce(adm.ccs_130, 0) as ccs_130,
  coalesce(adm.ccs_131, 0) as ccs_131,
  coalesce(adm.ccs_132, 0) as ccs_132,
  coalesce(adm.ccs_133, 0) as ccs_133,
  coalesce(adm.ccs_134, 0) as ccs_134,
  coalesce(adm.ccs_135, 0) as ccs_135,
  coalesce(adm.ccs_136, 0) as ccs_136,
  coalesce(adm.ccs_137, 0) as ccs_137,
  coalesce(adm.ccs_138, 0) as ccs_138,
  coalesce(adm.ccs_139, 0) as ccs_139,
  coalesce(adm.ccs_140, 0) as ccs_140,
  coalesce(adm.ccs_141, 0) as ccs_141,
  coalesce(adm.ccs_142, 0) as ccs_142,
  coalesce(adm.ccs_143, 0) as ccs_143,
  coalesce(adm.ccs_144, 0) as ccs_144,
  coalesce(adm.ccs_145, 0) as ccs_145,
  coalesce(adm.ccs_146, 0) as ccs_146,
  coalesce(adm.ccs_147, 0) as ccs_147,
  coalesce(adm.ccs_148, 0) as ccs_148,
  coalesce(adm.ccs_149, 0) as ccs_149,
  coalesce(adm.ccs_150, 0) as ccs_150,
  coalesce(adm.ccs_151, 0) as ccs_151,
  coalesce(adm.ccs_152, 0) as ccs_152,
  coalesce(adm.ccs_153, 0) as ccs_153,
  coalesce(adm.ccs_154, 0) as ccs_154,
  coalesce(adm.ccs_155, 0) as ccs_155,
  coalesce(adm.ccs_156, 0) as ccs_156,
  coalesce(adm.ccs_157, 0) as ccs_157,
  coalesce(adm.ccs_158, 0) as ccs_158,
  coalesce(adm.ccs_159, 0) as ccs_159,
  coalesce(adm.ccs_160, 0) as ccs_160,
  coalesce(adm.ccs_161, 0) as ccs_161,
  coalesce(adm.ccs_162, 0) as ccs_162,
  coalesce(adm.ccs_163, 0) as ccs_163,
  coalesce(adm.ccs_164, 0) as ccs_164,
  coalesce(adm.ccs_165, 0) as ccs_165,
  coalesce(adm.ccs_166, 0) as ccs_166,
  coalesce(adm.ccs_167, 0) as ccs_167,
  coalesce(adm.ccs_168, 0) as ccs_168,
  coalesce(adm.ccs_169, 0) as ccs_169,
  coalesce(adm.ccs_170, 0) as ccs_170,
  coalesce(adm.ccs_171, 0) as ccs_171,
  coalesce(adm.ccs_172, 0) as ccs_172,
  coalesce(adm.ccs_173, 0) as ccs_173,
  coalesce(adm.ccs_174, 0) as ccs_174,
  coalesce(adm.ccs_175, 0) as ccs_175,
  coalesce(adm.ccs_176, 0) as ccs_176,
  coalesce(adm.ccs_177, 0) as ccs_177,
  coalesce(adm.ccs_178, 0) as ccs_178,
  coalesce(adm.ccs_179, 0) as ccs_179,
  coalesce(adm.ccs_180, 0) as ccs_180,
  coalesce(adm.ccs_181, 0) as ccs_181,
  coalesce(adm.ccs_182, 0) as ccs_182,
  coalesce(adm.ccs_183, 0) as ccs_183,
  coalesce(adm.ccs_184, 0) as ccs_184,
  coalesce(adm.ccs_185, 0) as ccs_185,
  coalesce(adm.ccs_186, 0) as ccs_186,
  coalesce(adm.ccs_187, 0) as ccs_187,
  coalesce(adm.ccs_188, 0) as ccs_188,
  coalesce(adm.ccs_189, 0) as ccs_189,
  coalesce(adm.ccs_190, 0) as ccs_190,
  coalesce(adm.ccs_191, 0) as ccs_191,
  coalesce(adm.ccs_192, 0) as ccs_192,
  coalesce(adm.ccs_193, 0) as ccs_193,
  coalesce(adm.ccs_194, 0) as ccs_194,
  coalesce(adm.ccs_195, 0) as ccs_195,
  coalesce(adm.ccs_196, 0) as ccs_196,
  coalesce(adm.ccs_197, 0) as ccs_197,
  coalesce(adm.ccs_198, 0) as ccs_198,
  coalesce(adm.ccs_199, 0) as ccs_199,
  coalesce(adm.ccs_200, 0) as ccs_200,
  coalesce(adm.ccs_201, 0) as ccs_201,
  coalesce(adm.ccs_202, 0) as ccs_202,
  coalesce(adm.ccs_203, 0) as ccs_203,
  coalesce(adm.ccs_204, 0) as ccs_204,
  coalesce(adm.ccs_205, 0) as ccs_205,
  coalesce(adm.ccs_206, 0) as ccs_206,
  coalesce(adm.ccs_207, 0) as ccs_207,
  coalesce(adm.ccs_208, 0) as ccs_208,
  coalesce(adm.ccs_209, 0) as ccs_209,
  coalesce(adm.ccs_210, 0) as ccs_210,
  coalesce(adm.ccs_211, 0) as ccs_211,
  coalesce(adm.ccs_212, 0) as ccs_212,
  coalesce(adm.ccs_213, 0) as ccs_213,
  coalesce(adm.ccs_214, 0) as ccs_214,
  coalesce(adm.ccs_215, 0) as ccs_215,
  coalesce(adm.ccs_216, 0) as ccs_216,
  coalesce(adm.ccs_217, 0) as ccs_217,
  coalesce(adm.ccs_218, 0) as ccs_218,
  coalesce(adm.ccs_219, 0) as ccs_219,
  coalesce(adm.ccs_220, 0) as ccs_220,
  coalesce(adm.ccs_221, 0) as ccs_221,
  coalesce(adm.ccs_222, 0) as ccs_222,
  coalesce(adm.ccs_223, 0) as ccs_223,
  coalesce(adm.ccs_224, 0) as ccs_224,
  coalesce(adm.ccs_225, 0) as ccs_225,
  coalesce(adm.ccs_226, 0) as ccs_226,
  coalesce(adm.ccs_227, 0) as ccs_227,
  coalesce(adm.ccs_228, 0) as ccs_228,
  coalesce(adm.ccs_229, 0) as ccs_229,
  coalesce(adm.ccs_230, 0) as ccs_230,
  coalesce(adm.ccs_231, 0) as ccs_231,
  coalesce(adm.ccs_232, 0) as ccs_232,
  coalesce(adm.ccs_233, 0) as ccs_233,
  coalesce(adm.ccs_234, 0) as ccs_234,
  coalesce(adm.ccs_235, 0) as ccs_235,
  coalesce(adm.ccs_236, 0) as ccs_236,
  coalesce(adm.ccs_237, 0) as ccs_237,
  coalesce(adm.ccs_238, 0) as ccs_238,
  coalesce(adm.ccs_239, 0) as ccs_239,
  coalesce(adm.ccs_240, 0) as ccs_240,
  coalesce(adm.ccs_241, 0) as ccs_241,
  coalesce(adm.ccs_242, 0) as ccs_242,
  coalesce(adm.ccs_243, 0) as ccs_243,
  coalesce(adm.ccs_244, 0) as ccs_244,
  coalesce(adm.ccs_245, 0) as ccs_245,
  coalesce(adm.ccs_246, 0) as ccs_246,
  coalesce(adm.ccs_247, 0) as ccs_247,
  coalesce(adm.ccs_248, 0) as ccs_248,
  coalesce(adm.ccs_249, 0) as ccs_249,
  coalesce(adm.ccs_250, 0) as ccs_250,
  coalesce(adm.ccs_251, 0) as ccs_251,
  coalesce(adm.ccs_252, 0) as ccs_252,
  coalesce(adm.ccs_253, 0) as ccs_253,
  coalesce(adm.ccs_254, 0) as ccs_254,
  coalesce(adm.ccs_255, 0) as ccs_255,
  coalesce(adm.ccs_256, 0) as ccs_256,
  coalesce(adm.ccs_257, 0) as ccs_257,
  coalesce(adm.ccs_258, 0) as ccs_258,
  coalesce(adm.ccs_259, 0) as ccs_259,
  coalesce(adm.ccs_260, 0) as ccs_260,
  coalesce(adm.ccs_261, 0) as ccs_261,
  coalesce(adm.ccs_262, 0) as ccs_262,
  coalesce(adm.ccs_263, 0) as ccs_263,
  coalesce(adm.ccs_264, 0) as ccs_264,
  coalesce(adm.ccs_265, 0) as ccs_265,
  coalesce(adm.ccs_266, 0) as ccs_266,
  coalesce(adm.ccs_267, 0) as ccs_267,
  coalesce(adm.ccs_268, 0) as ccs_268,
  coalesce(adm.ccs_269, 0) as ccs_269,
  coalesce(adm.ccs_270, 0) as ccs_270,
  coalesce(adm.ccs_271, 0) as ccs_271,
  coalesce(adm.ccs_272, 0) as ccs_272,
  coalesce(adm.ccs_273, 0) as ccs_273,
  coalesce(adm.ccs_274, 0) as ccs_274,
  coalesce(adm.ccs_275, 0) as ccs_275,
  coalesce(adm.ccs_276, 0) as ccs_276,
  coalesce(adm.ccs_277, 0) as ccs_277,
  coalesce(adm.ccs_278, 0) as ccs_278,
  coalesce(adm.ccs_279, 0) as ccs_279,
  coalesce(adm.ccs_280, 0) as ccs_280,
  coalesce(adm.ccs_281, 0) as ccs_281
from model_demog as model_demog
  left join admissions_ccs_ohe as adm
    on model_demog.hadm_id = adm.hadm_id
;
