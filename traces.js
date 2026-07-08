window.TRACES = [
  {
    "patient_id": "S001",
    "patient_text": "A 54-year-old man with a history of chronic alcohol use presents with severe epigastric pain radiating to the back, nausea, and vomiting. Labs reveal markedly elevated serum lipase and amylase.",
    "extraction": [
      {
        "name": "Age",
        "value": "54 years",
        "evidence_quote": "54-year-old man"
      },
      {
        "name": "Sex",
        "value": "male",
        "evidence_quote": "54-year-old man"
      },
      {
        "name": "Alcohol use history",
        "value": "chronic alcohol use",
        "evidence_quote": "chronic alcohol use"
      },
      {
        "name": "Epigastric pain",
        "value": "severe, radiating to back",
        "evidence_quote": "severe epigastric pain radiating to the back"
      },
      {
        "name": "Nausea",
        "value": "present",
        "evidence_quote": "nausea"
      },
      {
        "name": "Vomiting",
        "value": "present",
        "evidence_quote": "vomiting"
      },
      {
        "name": "Serum lipase",
        "value": "markedly elevated",
        "evidence_quote": "markedly elevated serum lipase"
      },
      {
        "name": "Serum amylase",
        "value": "markedly elevated",
        "evidence_quote": "markedly elevated serum lipase and amylase"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06179459",
        "title": "Registry of Patients Undergoing Endoscopic Management of Pancreatic Fluid Collections",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 54-year-old man",
            "reasoning": "Patient age 54 exceeds minimum requirement of 18 years."
          },
          {
            "text": "Undergoing endoscopic treatment of pancreatic fluid collections",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette describes acute presentation; no mention of endoscopic treatment or pancreatic fluid collections."
          },
          {
            "text": "Age < 18 years",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "A 54-year-old man",
            "reasoning": "Patient is 54 years old; exclusion criterion (age < 18) does not apply."
          },
          {
            "text": "Patients who did not receive endoscopic treatment of pancreatic fluid collections",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided regarding whether endoscopic treatment was performed."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Age-eligible; endoscopic treatment plan unknown. Eligible if pancreatic fluid collections develop requiring intervention."
      },
      {
        "nct_id": "NCT06113419",
        "title": "Timing of CHolecystectomy In Severe PAncreatitis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥18 years",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 54-year-old man",
            "reasoning": "Patient age 54 exceeds minimum age ≥18 years"
          },
          {
            "text": "Diagnosis of pancreatitis according to Atlanta guidelines",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "severe epigastric pain radiating to back, markedly elevated serum lipase and amylase",
            "reasoning": "Clinical presentation and enzyme elevation satisfy Atlanta diagnostic criteria for pancreatitis"
          },
          {
            "text": "Moderately severe or severe pancreatitis (APACHE score ≥8 on admittance)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No APACHE score documented on admission"
          },
          {
            "text": "Biliary pancreatitis diagnosed on imaging (ultrasound, MRI, and/or CT)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No imaging results (ultrasound, MRI, CT) provided; etiology not specified"
          },
          {
            "text": "Tolerance of oral intake (24 hours of food consumption without emetic episodes) and pain ≤4/10 on visual analogue score",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "nausea, and vomiting",
            "reasoning": "Active vomiting at presentation; fails oral intake tolerance requirement"
          },
          {
            "text": "Pregnancy",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "54-year-old man",
            "reasoning": "Male patient; pregnancy exclusion criterion clearly not met"
          },
          {
            "text": "History of cholecystectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior surgical history documented"
          },
          {
            "text": "Pancreatitis-associated complication before laparoscopic cholecystectomy (compartment syndrome, bleeding, and/or need for peripancreatic collection drainage)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No data on compartment syndrome, bleeding, or peripancreatic collection drainage"
          },
          {
            "text": "Chronic pancreatitis",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": "chronic alcohol use",
            "reasoning": "Chronic alcohol use is risk factor but acute presentation; no documented chronic pancreatitis diagnosis"
          },
          {
            "text": "Active malignant disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No oncologic history provided"
          },
          {
            "text": "Septic shock",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No data on sepsis or septic shock status"
          },
          {
            "text": "Choledocholithiasis not resolved by ERCP, post-ERCP perforation, and post-ERCP concomitant pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No mention of choledocholithiasis, ERCP, or post-ERCP complications"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Meets AP diagnosis but fails oral tolerance and pain control (NOT_MET); may qualify after acute stabilization."
      },
      {
        "nct_id": "NCT06401577",
        "title": "Diabetes RElated to Acute Pancreatitis and Its Mechanisms: Metabolic Outcomes Using Novel CGM Metrics",
        "phase": "NA",
        "criteria": [
          {
            "text": "Diagnosis of acute pancreatitis (AP) 0-90 days prior to enrollment",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "severe epigastric pain radiating to the back, nausea, vomiting, markedly elevated serum lipase and amylase",
            "reasoning": "Classic AP presentation and labs; timing to enrollment and imaging confirmation not specified."
          },
          {
            "text": "Participant fully understands and is able to participate in all aspects of the study, including providing informed consent, completion of case report forms, telephone interviews, metabolic testing, and planned longitudinal follow-ups",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about patient's cognitive status or ability to participate in study procedures."
          },
          {
            "text": "Diagnosis of definite chronic pancreatitis (CP) at enrollment based on computed tomography (CT) scan, Magnetic Resonance Imaging (MRI), or Magnetic Resonance Cholangiopancreatography (MRCP) showing parenchymal or ductal calcifications or intraductal filling defects suggestive of calcifications",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No imaging results (CT/MRI/MRCP) provided to assess for chronic pancreatitis findings."
          },
          {
            "text": "Post-ERCP acute pancreatitis with hospitalization for less than 48 hours",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "chronic alcohol use presents with severe epigastric pain",
            "reasoning": "Alcohol-related AP; no evidence of prior ERCP. Patient does not meet this exclusion."
          },
          {
            "text": "Prior direct endoscopic necrosectomy of the pancreas or percutaneous necrosectomy or drainage of necrotic collection(s)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about prior pancreatic interventions or procedures."
          },
          {
            "text": "Pancreatic tumors, including ductal adenocarcinoma, neuroendocrine tumors, and metastasis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No imaging results provided to confirm absence of pancreatic malignancy."
          },
          {
            "text": "Confirmed or suspected cystic tumor associated with main pancreatic duct dilation, or believed to be the cause of acute pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No imaging results provided to assess for cystic lesions or duct changes."
          },
          {
            "text": "Prior pancreatic surgery, including distal pancreatectomy, pancreaticoduodenectomy, pancreatic necrosectomy, or Frey procedure",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No surgical history provided; prior pancreatic surgery status unknown."
          },
          {
            "text": "Severe systemic illness including history of solid organ transplant, AIDS, active cancer treatment within 12 months, chronic kidney disease with estimated glomerular filtration rate less than 30 or on dialysis prior to AP, decompensated cirrhosis, or life expectancy less than 12 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Chronic alcohol use noted; cirrhosis, transplant, AIDS, cancer, kidney disease status not documented."
          },
          {
            "text": "Known pregnancy at the time of enrollment",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "54-year-old man",
            "reasoning": "Male patient; pregnancy exclusion does not apply."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "AP diagnosis uncertain timing; post-ERCP pancreatitis exclusion met despite no ERCP mention in vignette."
      },
      {
        "nct_id": "NCT07144917",
        "title": "Immunoparalysis After Pancreaticoduodenectomy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Any patient undergoing a Pancreaticoduodenectomy in one of the four participating centers for a benign or malignant tumor of the pancreatic head",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "severe epigastric pain radiating to the back, nausea, and vomiting. Labs reveal markedly elevated serum lipase and amylase",
            "reasoning": "Acute pancreatitis presentation; no tumor or pancreaticoduodenectomy documented"
          },
          {
            "text": "Age < 18 years",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "54-year-old man",
            "reasoning": "Patient age 54 years, well above 18 years exclusion threshold"
          },
          {
            "text": "Pregnant, postpartum, or breastfeeding women",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "54-year-old man",
            "reasoning": "Male patient; pregnancy exclusion not applicable"
          },
          {
            "text": "Indication other than tumor-related (e.g., chronic pancreatitis)",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "chronic alcohol use presents with severe epigastric pain radiating to the back, nausea, and vomiting",
            "reasoning": "Acute pancreatitis from chronic alcohol; non-tumor-related indication"
          },
          {
            "text": "Patient with an infectious syndrome at the time of inclusion",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No infectious syndrome documented in clinical presentation"
          },
          {
            "text": "Preoperative immunosuppression",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No preoperative immunosuppression documented"
          },
          {
            "text": "Congenital or acquired immune deficiency",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No immune deficiency documented in history"
          },
          {
            "text": "Functional hyposplenism or asplenia, patient under long-term antibiotic prophylaxis for this reason",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No spleen dysfunction or prophylaxis documented"
          },
          {
            "text": "Patient with HIV (and CD4 < cells/mm³)",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No HIV documented in patient history"
          },
          {
            "text": "Aplasia defined by circulating neutrophil count < 500 cells/mm³",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Neutrophil count not provided in vignette"
          },
          {
            "text": "Corticosteroid therapy >10 mg/day or cumulative dose >700 mg prednisolone equivalent",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No corticosteroid therapy documented"
          },
          {
            "text": "Patient expected to receive immunosuppressive treatment within the first 7 postoperative days",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No immunosuppressive treatment planned"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Core inclusion NOT_MET: not undergoing pancreaticoduodenectomy; study inappropriate for acute medical pancreatitis."
      }
    ],
    "questions": [
      {
        "field": "Pancreatic imaging findings",
        "question": "What do imaging studies show about pancreatic structure, ductal dilation, or masses?",
        "why": "Affects 4 trial criteria; rules out malignancy, obstruction, chronic changes."
      },
      {
        "field": "Serious systemic comorbidities",
        "question": "Does he have diabetes, coronary disease, kidney disease, cirrhosis, or severe COPD?",
        "why": "Determines safety eligibility; high-risk comorbidities exclude from most trials."
      },
      {
        "field": "Biliary disease history",
        "question": "Any prior gallstones, cholecystectomy, or biliary obstruction?",
        "why": "Distinguishes biliary from alcohol etiology; affects management and trial eligibility."
      }
    ],
    "reeval": {
      "extended_record": "CT abdomen with contrast revealed pancreatic edema and enlargement with peripancreatic stranding consistent with acute pancreatitis. The main pancreatic duct measured 5 mm in diameter with mild ductal dilation; no focal masses or necrosis identified. Biochemically, fasting glucose was 156 mg/dL, creatinine 1.1 mg/dL indicating normal kidney function. Liver studies demonstrated elevated transaminases (AST 78 U/L, ALT 45 U/L) and GGT 142 U/L consistent with chronic liver disease, and prothrombin time 16.2 sec (INR 1.3) suggesting mild hepatic synthetic dysfunction; spider angiomata noted on chest wall examination. No prior cholecystectomy; right upper quadrant ultrasound identified no gallstones and no biliary ductal dilation. No documented diabetes prior to presentation, though glucose elevation suggests possible new impaired fasting glucose. No significant cardiac, pulmonary, or prior renal disease history reported.",
      "answers": [
        {
          "question": "What do imaging studies show about pancreatic structure, ductal dilation, or masses?",
          "answer": "CT imaging shows pancreatic edema and enlargement with peripancreatic stranding, mild main pancreatic duct dilation (5 mm), and no focal masses or necrosis.",
          "evidence_quote": "CT abdomen with contrast revealed pancreatic edema and enlargement with peripancreatic stranding consistent with acute pancreatitis. The main pancreatic duct measured 5 mm in diameter with mild ductal dilation; no focal masses or necrosis identified."
        },
        {
          "question": "Does he have diabetes, coronary disease, kidney disease, cirrhosis, or severe COPD?",
          "answer": "No prior diabetes documented though current fasting glucose 156 mg/dL; normal kidney function (creatinine 1.1 mg/dL); no significant cardiac or pulmonary history; clinical and biochemical evidence of cirrhosis including elevated liver enzymes, synthetic dysfunction, and spider angiomata.",
          "evidence_quote": "Liver studies demonstrated elevated transaminases (AST 78 U/L, ALT 45 U/L) and GGT 142 U/L consistent with chronic liver disease, and prothrombin time 16.2 sec (INR 1.3) suggesting mild hepatic synthetic dysfunction; spider angiomata noted on chest wall examination."
        },
        {
          "question": "Any prior gallstones, cholecystectomy, or biliary obstruction?",
          "answer": "No prior cholecystectomy and no gallstones on imaging; no biliary ductal dilation noted.",
          "evidence_quote": "No prior cholecystectomy; right upper quadrant ultrasound identified no gallstones and no biliary ductal dilation."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06113419",
          "criterion": "Biliary pancreatitis diagnosed on imaging (ultrasound, MRI, and/or CT)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "History of cholecystectomy",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Chronic pancreatitis",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Active malignant disease",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Septic shock",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Choledocholithiasis not resolved by ERCP, post-ERCP perforation, and post-ERCP concomitant pancreatitis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Diagnosis of definite chronic pancreatitis (CP) at enrollment based on computed tomography (CT) scan, Magnetic Resonance Imaging (MRI), or Magnetic Resonance Cholangiopancreatography (MRCP) showing parenchymal or ductal calcifications or intraductal filling defects suggestive of calcifications",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Pancreatic tumors, including ductal adenocarcinoma, neuroendocrine tumors, and metastasis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Confirmed or suspected cystic tumor associated with main pancreatic duct dilation, or believed to be the cause of acute pancreatitis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Severe systemic illness including history of solid organ transplant, AIDS, active cancer treatment within 12 months, chronic kidney disease with estimated glomerular filtration rate less than 30 or on dialysis prior to AP, decompensated cirrhosis, or life expectancy less than 12 months",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06179459",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Acute pancreatitis confirmed; eligibility depends on whether fluid collections develop requiring endoscopic drainage."
        },
        {
          "nct_id": "NCT06113419",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Trial requires biliary pancreatitis (patient has alcohol-related) and oral tolerance without vomiting; both failed."
        },
        {
          "nct_id": "NCT06401577",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Chronic alcohol history indicates chronic pancreatitis/cirrhosis, meeting trial's exclusion criteria for acute-AP-only study."
        },
        {
          "nct_id": "NCT07144917",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Trial requires pancreaticoduodenectomy for tumor; patient presenting with acute pancreatitis, not undergoing surgery."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S002",
    "patient_text": "A 29-year-old woman presents with intermittent palpitations, heat intolerance, and unintentional weight loss. Physical exam reveals a fine tremor, tachycardia, and a diffusely enlarged, non-tender thyroid gland.",
    "extraction": [
      {
        "name": "Age",
        "value": "29 years old",
        "evidence_quote": "29-year-old"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "woman"
      },
      {
        "name": "Palpitations",
        "value": "Intermittent palpitations",
        "evidence_quote": "intermittent palpitations"
      },
      {
        "name": "Heat intolerance",
        "value": "Present",
        "evidence_quote": "heat intolerance"
      },
      {
        "name": "Unintentional weight loss",
        "value": "Present",
        "evidence_quote": "unintentional weight loss"
      },
      {
        "name": "Tremor",
        "value": "Fine tremor",
        "evidence_quote": "fine tremor"
      },
      {
        "name": "Tachycardia",
        "value": "Present",
        "evidence_quote": "tachycardia"
      },
      {
        "name": "Thyroid size",
        "value": "Diffusely enlarged",
        "evidence_quote": "diffusely enlarged, non-tender thyroid gland"
      },
      {
        "name": "Thyroid tenderness",
        "value": "Non-tender",
        "evidence_quote": "non-tender"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT05461820",
        "title": "Effects of Different Treatment Schemes on the Regulation and Recurrence of Graves' Disease",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Graves hyperthyroidism (responsible for doctors' clinical diagnosis)",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "diffusely enlarged, non-tender thyroid gland; intermittent palpitations, heat intolerance, weight loss, fine tremor, tachycardia",
            "reasoning": "Clinical presentation classic for Graves but diagnostic confirmation not explicitly stated in vignette"
          },
          {
            "text": "Age 18-65, for both men and women",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 29-year-old woman",
            "reasoning": "Patient age 29 falls within inclusion range 18-65"
          },
          {
            "text": "Thyroid receptor antibody (TRAb) was positive",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "TRAb antibody test results not provided in vignette"
          },
          {
            "text": "Take part in this research voluntarily and sign the informed consent form",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about informed consent or voluntary participation"
          },
          {
            "text": "Those who have used glucocorticoid or other immunosuppressants for a long time within 3 months before being selected",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No medication or immunosuppressant history documented"
          },
          {
            "text": "Those who have participated in any other drug trials within 3 months before being selected",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior trial participation history provided"
          },
          {
            "text": "Patients with a history of malignant tumors",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No malignancy history documented in vignette"
          },
          {
            "text": "Ill-controlled hypertension: diastolic blood pressure≥100mmHg, systolic blood pressure ≥160 mmHg",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No blood pressure measurements provided"
          },
          {
            "text": "Blood routine: the total number of white blood cells < 3.0×10^9 or neutrophils < 1.5× 10^9",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No complete blood count or white cell/neutrophil values provided"
          },
          {
            "text": "Other thyroid diseases: such as subacute thyroiditis, thyroid nodules, high-function adenoma",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "diffusely enlarged, non-tender thyroid gland",
            "reasoning": "Diffuse non-tender goiter excludes nodules, thyroiditis, and adenoma"
          },
          {
            "text": "Alanine aminotransferase(ALT) or aspartate amino transferase(AST) is greater than 2 times of the normal upper limit; When ALT or AST is less than 2 times of the normal upper limit, and the test of hepatitis B two half-and-half positive",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No liver function tests or hepatitis B serology provided"
          },
          {
            "text": "Renal insufficiency: serum creatinine is higher than the upper limit of normal value",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No serum creatinine or renal function data provided"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Classic Graves' presentation (goiter, tremor, tachycardia, weight loss); age-eligible. Needs TRAb+ confirmation and laboratory baseline."
      },
      {
        "nct_id": "NCT06963203",
        "title": "Thyroidectomy for Graves' Disease or Amiodarone-induced Thyrotoxicosis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 29-year-old woman",
            "reasoning": "Patient age 29 satisfies ≥18 requirement"
          },
          {
            "text": "Undergoing surgical treatment for Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Clinical presentation suggests Graves' disease but surgical treatment status not mentioned"
          },
          {
            "text": "Biochemically confirmed hyperthyroidism or on specific medication for treatment of Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "intermittent palpitations, heat intolerance, unintentional weight loss, fine tremor, tachycardia, diffusely enlarged thyroid",
            "reasoning": "Classic hyperthyroid signs present; biochemical confirmation and medications not documented"
          },
          {
            "text": "Providing signed informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about informed consent status provided"
          },
          {
            "text": "Age < 18 years",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "A 29-year-old woman",
            "reasoning": "Patient age 29 does not satisfy excluded condition Age <18"
          },
          {
            "text": "Pregnant women",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Pregnancy status not mentioned in vignette"
          },
          {
            "text": "Unable or unwilling to provide informed consent due to language barriers or intellectual limitations",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about consent capacity or barriers"
          },
          {
            "text": "Undergoing concurrent parathyroidectomy for primary or secondary hyperparathyroidism, lymph node clearance, or redo surgery",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No mention of concurrent parathyroidectomy, lymph node clearance, or redo surgery"
          },
          {
            "text": "Surgical procedures performed for reasons other than Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No surgical procedures mentioned; indication cannot be determined"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Hyperthyroid features and age-eligible; undergoing thyroidectomy status unknown. Candidacy unclear without surgical treatment confirmation."
      },
      {
        "nct_id": "NCT05678374",
        "title": "Exploring Immunological Markers Associated With Mental Fatigue in Graves' Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "Graves' disease with positive TSH-receptor antibodies and thyroid hormones above the upper reference limit at diagnosis",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Diffusely enlarged thyroid, palpitations, tremor, tachycardia, heat intolerance, weight loss",
            "reasoning": "Clinical signs suggest Graves', but TSH-receptor antibodies and thyroid hormone levels not documented."
          },
          {
            "text": "Diagnosis 15 to 60 months ago. If recidive both episodes must have occurred within 15 months to 60 months",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No diagnosis date or timing history provided."
          },
          {
            "text": "Thyroid hormones within normal range without anti thyroid drugs",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No thyroid hormone levels or anti-thyroid medication status documented."
          },
          {
            "text": "No thyroid disease",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Diffusely enlarged, non-tender thyroid gland",
            "reasoning": "Patient has thyroid pathology, criterion requires no thyroid disease."
          },
          {
            "text": "Mental Fatigue Score ≤8 (cut off 10.5)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Mental Fatigue Score not documented."
          },
          {
            "text": "Mental Fatigue Score >13 and debut of symptoms of mental fatigue in parallel with debut of Graves' disease, without other obvious cause",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Mental Fatigue Score and symptom timing not documented."
          },
          {
            "text": "Multiple sclerosis, myalgic encephalomyelitis/chronic fatigue syndrome, any other neurological disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No neurological disease history provided."
          },
          {
            "text": "Traumatic brain injury with unconsciousness",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No traumatic brain injury history documented."
          },
          {
            "text": "Other disease strongly associated with fatigue",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Limited medical history for assessing other fatigue-associated diseases."
          },
          {
            "text": "Pregnancy and breast-feeding",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Pregnancy and breastfeeding status not mentioned."
          },
          {
            "text": "On-going or recent systemic treatment with steroids",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No current or recent steroid use documented."
          },
          {
            "text": "Radioiodine therapy within the last 18 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No radioiodine therapy history mentioned."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Requires euthyroid without meds and no thyroid disease; patient actively hyperthyroid newly presenting with Graves' features."
      },
      {
        "nct_id": "NCT06392906",
        "title": "Orbital Radiotherapy in Grave's Ophthalmopathy 1 Week vs 2 Weeks (OraGO-1 Trial)",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Active moderate to severe thyroid eye disease with CAS > 4 with or without diplopia before starting IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No thyroid eye disease, CAS score, or ophthalmology findings documented."
          },
          {
            "text": "Poor response to 3 doses of IVMP with CAS drop < 1",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No IVMP treatment history or CAS response data mentioned."
          },
          {
            "text": "CAS score > 3 after 3 doses of IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No CAS score or IVMP treatment course documented."
          },
          {
            "text": "Diplopia after 3 doses of IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No diplopia or IVMP therapy history documented."
          },
          {
            "text": "Graves' Ophthalmopathy with maintained euthyroidism",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "intermittent palpitations, heat intolerance, unintentional weight loss, fine tremor, tachycardia",
            "reasoning": "Patient presents with hyperthyroid symptoms, not euthyroid. No eye disease mentioned."
          },
          {
            "text": "Age 35 years or older",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "A 29-year-old woman",
            "reasoning": "Age 29 does not meet age ≥35 requirement."
          },
          {
            "text": "Non-pregnant",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Pregnancy status not addressed in vignette."
          },
          {
            "text": "Severe hypertension",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No blood pressure or hypertension data provided."
          },
          {
            "text": "Diabetic retinopathy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No diabetes history or retinal examination documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Patient 29 years old, trial requires age≥35. No thyroid eye disease mentioned; trial targets ophthalmopathy complications."
      }
    ],
    "questions": [
      {
        "field": "Treatment history and research participation",
        "question": "What thyroid treatments have you received, and have you participated in any previous clinical trials?",
        "why": "Affects 7 trial criteria; multiple trials exclude recent immunosuppressants or concurrent participation"
      },
      {
        "field": "Thyroid eye disease severity and ocular status",
        "question": "Have you experienced any eye symptoms (bulging eyes, double vision, eye pain) or been evaluated by an eye specialist?",
        "why": "Affects 5 trial criteria; severity determines eligibility and immunosuppressive therapy safety"
      },
      {
        "field": "Graves' disease diagnosis and TSH receptor antibody status",
        "question": "Has thyroid antibody testing confirmed your Graves' disease diagnosis?",
        "why": "Core inclusion criterion; antibody confirmation is essential for trial eligibility"
      }
    ],
    "reeval": {
      "extended_record": "Patient was initiated on methimazole 20 mg daily in January 2024 following diagnosis confirmation. She participated in a phase II trial of TSH-receptor antagonist therapy (TSHR-I-001) from March to August 2024, which she tolerated well with good symptom response. Currently managed with methimazole 10 mg daily with improved thyroid function (TSH 0.8 mIU/L, fT4 12.5 pmol/L on most recent testing in May 2025). She reports no prior radioactive iodine or surgical intervention. Regarding ocular symptoms, she experienced mild lid retraction and occasional eye fatigue beginning approximately 4 months post-diagnosis but denies diplopia, eye pain, or severe exophthalmos. Ophthalmology evaluation in August 2024 confirmed mild Graves' ophthalmopathy (clinical activity score 2/7) without optic nerve involvement. TSI was markedly elevated at 8.2 IU/L (ref <1.75) in February 2024, confirming Graves' disease diagnosis. TPO antibodies were negative at that time.",
      "answers": [
        {
          "question": "What thyroid treatments have you received, and have you participated in any previous clinical trials?",
          "answer": "Initiated on methimazole in January 2024; currently on 10 mg daily with good response. Participated in phase II TSH-receptor antagonist trial (TSHR-I-001) from March to August 2024. No radioactive iodine or surgery.",
          "evidence_quote": "Patient was initiated on methimazole 20 mg daily in January 2024 following diagnosis confirmation. She participated in a phase II trial of TSH-receptor antagonist therapy (TSHR-I-001) from March to August 2024, which she tolerated well with good symptom response."
        },
        {
          "question": "Have you experienced any eye symptoms (bulging eyes, double vision, eye pain) or been evaluated by an eye specialist?",
          "answer": "Mild lid retraction and occasional eye fatigue; denies diplopia, eye pain, or severe exophthalmos. Ophthalmology evaluation in August 2024 confirmed mild Graves' ophthalmopathy without optic nerve involvement.",
          "evidence_quote": "she experienced mild lid retraction and occasional eye fatigue beginning approximately 4 months post-diagnosis but denies diplopia, eye pain, or severe exophthalmos. Ophthalmology evaluation in August 2024 confirmed mild Graves' ophthalmopathy (clinical activity score 2/7) without optic nerve involvement."
        },
        {
          "question": "Has thyroid antibody testing confirmed your Graves' disease diagnosis?",
          "answer": "Yes. TSI markedly elevated at 8.2 IU/L (reference <1.75) in February 2024, confirming Graves' disease. TPO antibodies were negative.",
          "evidence_quote": "TSI was markedly elevated at 8.2 IU/L (ref <1.75) in February 2024, confirming Graves' disease diagnosis. TPO antibodies were negative at that time."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT05461820",
          "criterion": "Graves hyperthyroidism (responsible for doctors' clinical diagnosis)",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Thyroid receptor antibody (TRAb) was positive",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Those who have used glucocorticoid or other immunosuppressants for a long time within 3 months before being selected",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Those who have participated in any other drug trials within 3 months before being selected",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06963203",
          "criterion": "Undergoing surgical treatment for Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06963203",
          "criterion": "Biochemically confirmed hyperthyroidism or on specific medication for treatment of Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06963203",
          "criterion": "Undergoing concurrent parathyroidectomy for primary or secondary hyperparathyroidism, lymph node clearance, or redo surgery",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06963203",
          "criterion": "Surgical procedures performed for reasons other than Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Graves' disease with positive TSH-receptor antibodies and thyroid hormones above the upper reference limit at diagnosis",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "On-going or recent systemic treatment with steroids",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Radioiodine therapy within the last 18 months",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "Active moderate to severe thyroid eye disease with CAS > 4 with or without diplopia before starting IVMP",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "Poor response to 3 doses of IVMP with CAS drop < 1",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "CAS score > 3 after 3 doses of IVMP",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "Diplopia after 3 doses of IVMP",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "Diabetic retinopathy",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT05461820",
          "rank": 1,
          "eligibility": "INELIGIBLE",
          "rationale": "Graves' disease confirmed (TRAb+, age MET). Excluded: recent glucocorticoid/immunosuppressant and concurrent trial within 3mo."
        },
        {
          "nct_id": "NCT06963203",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Biochemically confirmed hyperthyroidism matches. Trial requires active surgical treatment; patient not undergoing thyroidectomy."
        },
        {
          "nct_id": "NCT05678374",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Active Graves' hyperthyroidism; trial requires thyroid-healthy post-Graves' state. Also excluded: steroid/radioiodine therapy."
        },
        {
          "nct_id": "NCT06392906",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Age 29 below 35 minimum. No thyroid eye disease or prior IVMP history. Also excluded: diabetic retinopathy."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S003",
    "patient_text": "A 7-year-old boy with a 3-week history of periorbital edema and frothy urine. Urinalysis shows heavy proteinuria without hematuria, and serum albumin is low.",
    "extraction": [
      {
        "name": "age",
        "value": "7 years old",
        "evidence_quote": "7-year-old"
      },
      {
        "name": "sex",
        "value": "male",
        "evidence_quote": "boy"
      },
      {
        "name": "symptom_periorbital_edema",
        "value": "periorbital edema",
        "evidence_quote": "periorbital edema"
      },
      {
        "name": "symptom_duration",
        "value": "3-week history",
        "evidence_quote": "3-week history"
      },
      {
        "name": "symptom_frothy_urine",
        "value": "frothy urine",
        "evidence_quote": "frothy urine"
      },
      {
        "name": "urinalysis_proteinuria",
        "value": "heavy proteinuria",
        "evidence_quote": "heavy proteinuria"
      },
      {
        "name": "urinalysis_hematuria",
        "value": "absent",
        "evidence_quote": "without hematuria"
      },
      {
        "name": "serum_albumin",
        "value": "low",
        "evidence_quote": "serum albumin is low"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06607991",
        "title": "Blinatumomab for CNI-Resistant/Intolerant SRNS in Children",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Age between 2 and 17 years, regardless of gender",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "7-year-old",
            "reasoning": "Patient age falls within inclusion range of 2-17 years"
          },
          {
            "text": "Steroid-resistant nephrotic syndrome (SRNS) per 2021 KDIGO definition",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "heavy proteinuria without hematuria, and serum albumin is low",
            "reasoning": "Nephrotic syndrome evident but steroid resistance status unknown"
          },
          {
            "text": "Calcineurin inhibitor-resistant after ≥6 months of adequate dosing, OR calcineurin inhibitor-intolerant with documented contraindications, OR inadequate response or disease relapse after treatment with ≥2 other immunosuppressive agents",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior immunosuppressive treatment history documented"
          },
          {
            "text": "Renal biopsy confirms minimal change disease (MCD) or focal segmental glomerulosclerosis (FSGS)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No renal biopsy results provided in vignette"
          },
          {
            "text": "eGFR <60 mL/min/1.73 m² using the modified Bedside Schwartz formula",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No eGFR or creatinine data documented"
          },
          {
            "text": "Renal biopsy confirms IgA nephropathy, membranous nephropathy, or membranoproliferative glomerulonephritis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No renal biopsy pathology documented"
          },
          {
            "text": "Genetic nephropathy confirmed by genetic testing",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No genetic testing results documented"
          },
          {
            "text": "Stroke or seizure within 6 months prior to screening, or other active central nervous system disorders",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "periorbital edema and frothy urine",
            "reasoning": "No documented stroke, seizure, or active CNS disorder"
          },
          {
            "text": "Severe congenital heart disease, acute myocardial infarction within 6 months, severe arrhythmias, pericardial effusion, myocarditis, or unstable vital signs requiring vasopressors to maintain blood pressure",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No cardiac assessment or vital signs documented"
          },
          {
            "text": "Positive for hepatitis B surface antigen or hepatitis B core antibody with hepatitis B virus DNA above normal range, hepatitis C virus antibodies with hepatitis C virus RNA above normal range, HIV antibodies, syphilis, or cytomegalovirus DNA",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No infectious disease screening documented"
          },
          {
            "text": "Moderate to severe neutropenia (≤1.0×10⁹/L), hemoglobin ≤90 g/L, thrombocytopenia (≤75×10⁹/L), or liver dysfunction (ALT, AST, or bilirubin >2.5 times the upper limit of normal)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No blood counts or liver function tests documented"
          },
          {
            "text": "Positive blood pregnancy test",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "7-year-old boy",
            "reasoning": "Male patient; pregnancy not applicable"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 1,
        "rationale": "7-year-old with nephrotic syndrome fits pediatric SRNS trial. Exclusion verdicts (stroke/seizure, pregnancy) suspect for male child."
      },
      {
        "nct_id": "NCT04571658",
        "title": "NEPTUNE Match Study",
        "phase": "NA",
        "criteria": [
          {
            "text": "Consented and eligible participant in the biopsied or non-biopsied cohorts of the NEPTUNE observational study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of NEPTUNE enrollment status or consent status in vignette."
          },
          {
            "text": "Potentially eligible for the NEPTUNE Match partnering trials",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about trial eligibility assessment or partnering trial criteria applied."
          },
          {
            "text": "Regular nephrology healthcare provided at a NEPTUNE study site",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Care location and NEPTUNE study site affiliation not documented in vignette."
          },
          {
            "text": "Willing and able to consent, and as appropriate assent, to participate in NEPTUNE Match",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of guardian willingness or ability to consent/assent."
          },
          {
            "text": "Currently non-NEPTUNE observational study participant",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "NEPTUNE observational study participation status not documented."
          },
          {
            "text": "Non-English or non-Spanish speaking",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Patient/guardian language preference or capabilities not documented in vignette."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Insufficient data; registry may match patient if previously NEPTUNE-enrolled. Renal presentation consistent with candidacy."
      },
      {
        "nct_id": "NCT06162546",
        "title": "ARREST-NEPHROSIS - Austrian Resistant Nephrotic Syndrome Treatment Response Registry and Biobank",
        "phase": "NA",
        "criteria": [
          {
            "text": "Resistant to standard Immunosuppressive agents (if clinically indicated, e.g. primary/non-genetic forms)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on prior immunosuppressive treatment or response"
          },
          {
            "text": "Persistent urinary protein-to-creatinine (UP/C) ratio >1.0 g/g",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "heavy proteinuria",
            "reasoning": "Heavy proteinuria noted; specific UP/C ratio value not quantified"
          },
          {
            "text": "eGFR > 30 ml/min per 1.73 m2",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No kidney function or eGFR data provided"
          },
          {
            "text": "Confirmed diagnosis by biopsy or disease-causing genetic mutation associated with nephrotic syndrome",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "periorbital edema, frothy urine, heavy proteinuria, low serum albumin",
            "reasoning": "Classic nephrotic presentation evident; biopsy or genetic confirmation not documented"
          },
          {
            "text": "Inability or unwillingness to comply with repeated assessments",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on patient compliance or willingness"
          },
          {
            "text": "Objections against participation at discretion of the investigator",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on investigator objections"
          },
          {
            "text": "Secondary nephrotic syndrome",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No secondary causes documented; primary nephrotic presentation"
          },
          {
            "text": "Steroid-dependence or frequently relapsing disease, unless complete remission achieved",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior treatment history or relapse pattern documented"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Patient likely primary nephrotic syndrome; trial excludes secondary NS. Resistance status unknown; steroid response untested."
      },
      {
        "nct_id": "NCT06334692",
        "title": "Autoantibodies Against-nephrin in Idiopathic Nephrotic Syndrome",
        "phase": "NA",
        "criteria": [
          {
            "text": "Adult (>18 years) males and females",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "7-year-old boy",
            "reasoning": "Patient is 7 years old; criterion requires adults >18 years"
          },
          {
            "text": "Patients with biopsy-proven idiopathic MCD or FSGS (cases)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no mention of kidney biopsy or pathologic diagnosis"
          },
          {
            "text": "Patients with biopsy-proven idiopathic membranous nephropathy (controls)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No biopsy or membranous nephropathy diagnosis documented in vignette"
          },
          {
            "text": "Patients who provided consent to store their samples in the certified CRB biobank",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no information regarding consent or biobank participation"
          },
          {
            "text": "Reasonable possibility of a secondary cause of NS (for cases) or MN (for controls) at time of blood collections",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": "7-year-old boy with periorbital edema, frothy urine, heavy proteinuria, low albumin",
            "reasoning": "Classic primary NS presentation; no secondary causes documented, but complete workup unspecified"
          },
          {
            "text": "Active viral or bacterial infections at time of blood collections",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no information about active viral or bacterial infections"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Adult-only trial (>18 years); 7-year-old patient fails inclusion. Age mismatch is definitive exclusion."
      }
    ],
    "questions": [
      {
        "field": "Renal biopsy findings and pathological diagnosis",
        "question": "Has a renal biopsy been performed? If so, what was the pathological diagnosis (minimal change disease, focal segmental glomerulosclerosis, membranous nephropathy, IgA nephropathy, MPGN, or other)?",
        "why": "Pathological diagnosis required for all trial cohorts; determines treatment eligibility"
      },
      {
        "field": "Prior immunosuppressive treatment and steroid/CNI responsiveness",
        "question": "Has the patient received corticosteroid therapy? If yes, duration and response (complete remission, partial response, or steroid-resistant)?",
        "why": "Steroid responsiveness categorizes into steroid-responsive or resistant disease trials"
      },
      {
        "field": "Quantified renal function (eGFR or serum creatinine)",
        "question": "What is the most recent serum creatinine level and calculated eGFR?",
        "why": "Multiple trials have specific eGFR thresholds (>30, <60) for safety assessment"
      }
    ],
    "reeval": {
      "extended_record": "Renal ultrasound at presentation was normal without evidence of hydronephrosis. Renal biopsy performed at week 2 of hospitalization revealed minimal change disease (MCD) with intact glomerular basement membrane and no deposits on immunofluorescence. The patient was initiated on prednisone 60 mg/day (approximately 2 mg/kg/day) at hospital admission. After 10 days of corticosteroid therapy, urine protein decreased to 1+ on dipstick and periorbital edema began to resolve. By week 3 of prednisone treatment, the patient achieved complete remission with urine dipstick negative for protein and clinical resolution of edema. Most recent serum creatinine obtained 4 days ago is 0.35 mg/dL with calculated eGFR of 128 mL/min/1.73m² using Schwartz formula, indicating preserved renal function. Serum albumin has improved to 3.2 g/dL. Plan is to continue prednisone with gradual taper over 8 weeks.",
      "answers": [
        {
          "question": "Has a renal biopsy been performed? If so, what was the pathological diagnosis (minimal change disease, focal segmental glomerulosclerosis, membranous nephropathy, IgA nephropathy, MPGN, or other)?",
          "answer": "Yes, renal biopsy performed at week 2 of hospitalization revealed minimal change disease (MCD) with intact glomerular basement membrane and no deposits on immunofluorescence.",
          "evidence_quote": "Renal biopsy performed at week 2 of hospitalization revealed minimal change disease (MCD) with intact glomerular basement membrane and no deposits on immunofluorescence."
        },
        {
          "question": "Has the patient received corticosteroid therapy? If yes, duration and response (complete remission, partial response, or steroid-resistant)?",
          "answer": "Yes, prednisone 60 mg/day initiated at hospital admission; achieved complete remission by week 3 of treatment.",
          "evidence_quote": "The patient was initiated on prednisone 60 mg/day (approximately 2 mg/kg/day) at hospital admission. After 10 days of corticosteroid therapy, urine protein decreased to 1+ on dipstick and periorbital edema began to resolve. By week 3 of prednisone treatment, the patient achieved complete remission with urine dipstick negative for protein and clinical resolution of edema."
        },
        {
          "question": "What is the most recent serum creatinine level and calculated eGFR?",
          "answer": "Most recent serum creatinine is 0.35 mg/dL with calculated eGFR of 128 mL/min/1.73m².",
          "evidence_quote": "Most recent serum creatinine obtained 4 days ago is 0.35 mg/dL with calculated eGFR of 128 mL/min/1.73m² using Schwartz formula"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06607991",
          "criterion": "Steroid-resistant nephrotic syndrome (SRNS) per 2021 KDIGO definition",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Renal biopsy confirms minimal change disease (MCD) or focal segmental glomerulosclerosis (FSGS)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "eGFR <60 mL/min/1.73 m² using the modified Bedside Schwartz formula",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Renal biopsy confirms IgA nephropathy, membranous nephropathy, or membranoproliferative glomerulonephritis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06162546",
          "criterion": "eGFR > 30 ml/min per 1.73 m2",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06162546",
          "criterion": "Steroid-dependence or frequently relapsing disease, unless complete remission achieved",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06334692",
          "criterion": "Patients with biopsy-proven idiopathic MCD or FSGS (cases)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06334692",
          "criterion": "Patients with biopsy-proven idiopathic membranous nephropathy (controls)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT04571658",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Registry-based match study; unknown NEPTUNE cohort participation status. No confirmed disqualifying barriers."
        },
        {
          "nct_id": "NCT06607991",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "SRNS not established (inclusion NOT_MET); eGFR <60 (exclusion MET). CNS disorder exclusion also met."
        },
        {
          "nct_id": "NCT06162546",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Secondary nephrotic syndrome (exclusion MET). Steroid-dependence/frequent relapse (exclusion MET). Registry targets primary SRNS only."
        },
        {
          "nct_id": "NCT06334692",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Adult age >18 required (inclusion NOT_MET). Patient age 7; no pediatric arm. Absolute disqualification."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S004",
    "patient_text": "A 68-year-old man with a long smoking history presents with painless gross hematuria. CT urography reveals a mass in the bladder wall.",
    "extraction": [
      {
        "name": "Age",
        "value": "68",
        "evidence_quote": "68-year-old"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "man"
      },
      {
        "name": "Smoking history",
        "value": "Long smoking history",
        "evidence_quote": "long smoking history"
      },
      {
        "name": "Chief complaint",
        "value": "Painless gross hematuria",
        "evidence_quote": "painless gross hematuria"
      },
      {
        "name": "Hematuria character",
        "value": "Gross hematuria",
        "evidence_quote": "gross hematuria"
      },
      {
        "name": "Imaging study",
        "value": "CT urography",
        "evidence_quote": "CT urography"
      },
      {
        "name": "Imaging finding",
        "value": "Mass in bladder wall",
        "evidence_quote": "mass in the bladder wall"
      },
      {
        "name": "Mass location",
        "value": "Bladder wall",
        "evidence_quote": "bladder wall"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06493370",
        "title": "Intravenous Ascorbate Plus Gemcitabine/Carboplatin: A Novel and Cost-Effective Alternative With Evident Efficacy in Patients With Muscle Invasive Bladder Cancer",
        "phase": "PHASE2",
        "criteria": [
          {
            "text": "Age ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "Age: 68",
            "reasoning": "Patient 68 years old, well above 18-year threshold"
          },
          {
            "text": "ECOG Performance Status 0 - 2",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No ECOG performance status documented"
          },
          {
            "text": "Muscle invasive bladder cancer that is cisplatin-ineligible or declined based on Galsky criteria",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Mass in bladder wall",
            "reasoning": "Imaging shows bladder mass but lacks pathologic diagnosis and muscle invasion confirmation"
          },
          {
            "text": "Absolute Neutrophil Count > 1.5K/UL",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No absolute neutrophil count value provided"
          },
          {
            "text": "Platelets > 100K/UL",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No platelet count value documented"
          },
          {
            "text": "Hemoglobin ≥ 9 g/dL",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No hemoglobin value; hematuria present but labs absent"
          },
          {
            "text": "Serum creatinine ≤ 1.5 x upper limit of normal or calculated creatinine clearance ≥ 30 mL/min using the Cockcroft-Gault equation",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No serum creatinine or creatinine clearance documented"
          },
          {
            "text": "Normal Glucose-6-phosphate dehydrogenase (G6PD) status",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No G6PD testing results provided"
          },
          {
            "text": "Pregnant or breastfeeding",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Sex: Male",
            "reasoning": "Male patient cannot be pregnant or breastfeeding; exclusion does not apply"
          },
          {
            "text": "Active Grade 3 or 4 (per CTCAE Version 5.0) viral, bacterial, or fungal infection within 2 weeks prior to first dose of study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of recent infections or CTCAE grades"
          },
          {
            "text": "Uncontrolled intercurrent illness, including ongoing or active infection, symptomatic congestive heart failure, uncontrolled hypertension, unstable angina pectoris, cardiac arrhythmia, interstitial lung disease, or serious chronic gastrointestinal conditions associated with diarrhea",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No comorbidities or intercurrent illnesses documented in vignette"
          },
          {
            "text": "Histology of pure adenocarcinoma, pure squamous cell carcinoma, or pure small cell carcinoma in the TURBT sample",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No histopathology or TURBT results available; imaging only"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "68yo male MIBC presentation (hematuria, wall mass). Cisplatin-ineligible status unclear; requires ECOG, renal function, labs, histology confirmation."
      },
      {
        "nct_id": "NCT06709196",
        "title": "Clinical Trial Testing Whether Targeted Antibiotic Prophylaxis Can Reduce Infections After Cystectomy Compared to Empiric Prophylaxis",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Age at surgery ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 68-year-old man",
            "reasoning": "Age 68 exceeds minimum requirement of 18 years"
          },
          {
            "text": "Ability to understand and sign an informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no information about cognitive status or consent capacity"
          },
          {
            "text": "Malignant or benign indication for undergoing cystectomy",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "Mass in bladder wall; painless gross hematuria",
            "reasoning": "Bladder mass with hematuria indicates malignancy requiring cystectomy"
          },
          {
            "text": "Planned ileal conduit as urinary diversion",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about planned urinary diversion procedure type"
          },
          {
            "text": "Previous severe allergic reaction to antimicrobial treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No allergy or antimicrobial reaction history documented"
          },
          {
            "text": "Long-term prophylactic antibiotic treatment which is expected to be continued after the cystectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about current or planned antibiotic prophylaxis"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Bladder malignancy meets cystectomy indication. Surgical approach, antibiotic allergies, long-term prophylactic antibiotic use unknown."
      },
      {
        "nct_id": "NCT04916990",
        "title": "Improving Care for Rural Patients With Solid Tumors",
        "phase": "NA",
        "criteria": [
          {
            "text": "Male and female adults 18 years of age or older",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "Age: 68",
            "reasoning": "Patient is 68 years old, adult requirement met"
          },
          {
            "text": "English or Spanish speaking",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Language ability not documented in vignette"
          },
          {
            "text": "Receives cancer treatment at UCH-Aurora, UCH-Highlands Ranch, UCHealth North, UCHealth South-UCHealth Memorial Hospital, UCHealth Parkview Hospital, San Juan Cancer Center, RMCC-Pueblo, SCL-St. Mary's, or Parkview Medical Center",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Treatment facility location not specified"
          },
          {
            "text": "Diagnosed with lung cancer (small cell lung cancer or non-small cell lung cancer) with ICD-O codes C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, or C33.9",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Mass in bladder wall",
            "reasoning": "Patient has bladder cancer, not lung cancer"
          },
          {
            "text": "Diagnosed with head and neck squamous cell carcinoma (HNSCC) with specified ICD-O codes for oral cavity, oropharynx, hypopharynx, or larynx",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Mass in bladder wall",
            "reasoning": "Patient has bladder cancer, not head/neck carcinoma"
          },
          {
            "text": "Diagnosed with breast cancer (ICD-O codes C50.0, C50.1, C50.2, C50.3, C50.4, C50.5, C50.6, C50.8, C50.9), cervical cancer (ICD-O codes C53.0, C53.1, C53.8, C53.9), colorectal cancer (ICD-O codes C18, C20), or bladder cancer (ICD-O code C67.9)",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "Mass in bladder wall",
            "reasoning": "Imaging findings consistent with bladder cancer diagnosis"
          },
          {
            "text": "Will receive surgery, radiation therapy, chemotherapy, or combination of modalities including neoadjuvant and adjuvant therapy",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Treatment plan details not documented"
          },
          {
            "text": "Rural and medically underserved, defined as residing in a rural county with RUCC code 4-9 AND meeting health professional shortage area or medically underserved area/population criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Rural status and medical underservice criteria not documented"
          },
          {
            "text": "Uninsured (no public or private insurance) OR underinsured (public insurance only OR 10% or more of annual income spent on out-of-pocket medical expenses)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Insurance status not documented in vignette"
          },
          {
            "text": "Age under 18 years old",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Age: 68",
            "reasoning": "Patient age 68 excludes the under-18 exclusion criterion"
          },
          {
            "text": "Has already initiated curative treatment for the current episode of cancer",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Curative treatment initiation status not documented"
          },
          {
            "text": "From vulnerable populations (inmates, individuals on probation, homeless individuals, or pregnant individuals) or decisionally-challenged with cognitive or personality impairment, suicidal ideation, or intoxication at time of consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vulnerable population or decisional impairment status not documented"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 3,
        "rationale": "Bladder cancer qualifies as solid tumor diagnosis. Rural/medically underserved status, insurance coverage, treatment facility access unknown."
      },
      {
        "nct_id": "NCT05944237",
        "title": "HTL0039732 in Participants With Advanced Solid Tumours",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Histologically or cytologically proven advanced solid tumour, refractory to conventional treatment, or for which no further conventional therapy is considered appropriate by the Investigator or is declined by the potential participant",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Imaging shows lesion; no histological/cytological confirmation or treatment history provided."
          },
          {
            "text": "At least 1 measurable lesion according to RECIST v1.1, which (in the Investigator's opinion) has had objective radiological progression on or after the last therapy",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Lesion present on CT but no RECIST v1.1 assessment or prior progression documented."
          },
          {
            "text": "Life expectancy of at least 12 weeks",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No clinical data on life expectancy provided."
          },
          {
            "text": "Eastern Cooperative Oncology Group performance status of 0 or 1",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No ECOG performance status documented."
          },
          {
            "text": "Aged 18 years or over at the time consent is given",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 68-year-old man",
            "reasoning": "Patient age 68 clearly exceeds minimum 18 years."
          },
          {
            "text": "Radiotherapy (except for palliative reasons), chemotherapy, non chemotherapy systemic anti-cancer therapy or investigational medicinal products during the 4 weeks prior to enrolment; or first dose of an immunotherapy during the previous 12 weeks before first dose of HTL0039732",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on prior or recent anti-cancer treatments."
          },
          {
            "text": "Any central nervous system metastases (unless potential participants have had local therapy and are asymptomatic, radiologically stable and have been off steroids for ≥4 weeks prior to enrolment)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No mention of central nervous system involvement."
          },
          {
            "text": "Ongoing toxic manifestations of previous treatments that are Grade >1 per CTCAE v5.0",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of prior treatment toxicities."
          },
          {
            "text": "Known history of current or latent tuberculosis, HIV or Hepatitis B or C infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on TB, HIV, or Hepatitis B/C status."
          },
          {
            "text": "Prior treatment with EP4 inhibitor",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior treatment history documented."
          },
          {
            "text": "Significant cardiovascular disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Smoking history noted; no explicit cardiovascular disease assessment provided."
          },
          {
            "text": "Active autoimmune disease requiring systemic treatment in the 2 years prior to enrolment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on autoimmune disease history."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 4,
        "rationale": "Solid tumor present; phase 1 requires advanced/refractory status. ECOG performance, life expectancy, prior treatment history undefined."
      }
    ],
    "questions": [
      {
        "field": "Lab values (CBC, renal function, G6PD status)",
        "question": "What are the patient's current CBC (hemoglobin, ANC, platelets) and renal function (serum creatinine, calculated GFR) values?",
        "why": "Required for assessing safety baseline and trial eligibility thresholds"
      },
      {
        "field": "Tumor histology and invasiveness",
        "question": "Has tissue biopsy confirmed the diagnosis, and what is the histology type and depth of invasion (muscular involvement)?",
        "why": "Determines trial eligibility and appropriate treatment strategy"
      },
      {
        "field": "Comorbidities and intercurrent illness",
        "question": "Does the patient have any uncontrolled cardiac, pulmonary, GI, or autoimmune disease requiring exclusion assessment?",
        "why": "Trials exclude patients with uncontrolled comorbidities; need baseline"
      }
    ],
    "reeval": {
      "extended_record": "Cystoscopy with bladder biopsy confirmed high-grade urothelial carcinoma with invasion into muscularis propria, consistent with T2 disease. Recent labs: hemoglobin 10.2 g/dL, ANC 7,200/μL, platelets 245,000/μL, serum creatinine 1.1 mg/dL, calculated GFR 65 mL/min/1.73m² indicating Stage 2 chronic kidney disease. Cardiac exam without murmurs or signs of heart failure; ECG shows normal sinus rhythm. Chest X-ray clear with no COPD exacerbation; baseline FEV₁ 68% predicted. Abdomen soft, no hepatomegaly. No active gastrointestinal symptoms; prior upper endoscopy unremarkable. No history of autoimmune or connective tissue disease. Patient suitable for neoadjuvant chemotherapy or radical cystectomy.",
      "answers": [
        {
          "question": "What are the patient's current CBC (hemoglobin, ANC, platelets) and renal function (serum creatinine, calculated GFR) values?",
          "answer": "Hemoglobin 10.2 g/dL (mild anemia), ANC 7,200/μL, platelets 245,000/μL, serum creatinine 1.1 mg/dL, GFR 65 mL/min/1.73m² (Stage 2 CKD).",
          "evidence_quote": "hemoglobin 10.2 g/dL, ANC 7,200/μL, platelets 245,000/μL, serum creatinine 1.1 mg/dL, calculated GFR 65 mL/min/1.73m²"
        },
        {
          "question": "Has tissue biopsy confirmed the diagnosis, and what is the histology type and depth of invasion (muscular involvement)?",
          "answer": "Yes, biopsy confirmed high-grade urothelial carcinoma with muscularis propria invasion (T2 disease).",
          "evidence_quote": "Cystoscopy with bladder biopsy confirmed high-grade urothelial carcinoma with invasion into muscularis propria, consistent with T2 disease"
        },
        {
          "question": "Does the patient have any uncontrolled cardiac, pulmonary, GI, or autoimmune disease requiring exclusion assessment?",
          "answer": "No uncontrolled comorbidities noted. Cardiac exam normal, chest X-ray clear, no active GI symptoms, no autoimmune history.",
          "evidence_quote": "Cardiac exam without murmurs or signs of heart failure; ECG shows normal sinus rhythm. Chest X-ray clear with no COPD exacerbation; baseline FEV₁ 68% predicted. Abdomen soft, no hepatomegaly. No active gastrointestinal symptoms; prior upper endoscopy unremarkable. No history of autoimmune or connective tissue disease"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06493370",
          "criterion": "Absolute Neutrophil Count > 1.5K/UL",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Platelets > 100K/UL",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Hemoglobin ≥ 9 g/dL",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Serum creatinine ≤ 1.5 x upper limit of normal or calculated creatinine clearance ≥ 30 mL/min using the Cockcroft-Gault equation",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Uncontrolled intercurrent illness, including ongoing or active infection, symptomatic congestive heart failure, uncontrolled hypertension, unstable angina pectoris, cardiac arrhythmia, interstitial lung disease, or serious chronic gastrointestinal conditions associated with diarrhea",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Histology of pure adenocarcinoma, pure squamous cell carcinoma, or pure small cell carcinoma in the TURBT sample",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05944237",
          "criterion": "Histologically or cytologically proven advanced solid tumour, refractory to conventional treatment, or for which no further conventional therapy is considered appropriate by the Investigator or is declined by the potential participant",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05944237",
          "criterion": "At least 1 measurable lesion according to RECIST v1.1, which (in the Investigator's opinion) has had objective radiological progression on or after the last therapy",
          "before": "UNCERTAIN",
          "after": "UNKNOWN"
        },
        {
          "nct_id": "NCT05944237",
          "criterion": "Significant cardiovascular disease",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05944237",
          "criterion": "Active autoimmune disease requiring systemic treatment in the 2 years prior to enrolment",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06709196",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Bladder cancer patient suitable for cystectomy; confirmation needed on ileal conduit plan and hospital location."
        },
        {
          "nct_id": "NCT04916990",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Bladder cancer inclusion met; missing rural/underserved status, insurance status, language, and treatment modality details."
        },
        {
          "nct_id": "NCT06493370",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "MIBC cisplatin-ineligible appropriate; multiple exclusions flagged (uncontrolled illness, histology); data quality issues present."
        },
        {
          "nct_id": "NCT05944237",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Tumor not advanced/refractory (inclusion NOT_MET); significant cardiovascular and active autoimmune disease exclusions met."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S005",
    "patient_text": "A 34-year-old woman presents with recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia.",
    "extraction": [
      {
        "name": "Age",
        "value": "34 years old",
        "evidence_quote": "34-year-old woman"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "34-year-old woman"
      },
      {
        "name": "Chief Complaint",
        "value": "Recurrent episodes of severe unilateral throbbing headache",
        "evidence_quote": "recurrent episodes of severe unilateral throbbing headache"
      },
      {
        "name": "Headache Quality",
        "value": "Throbbing",
        "evidence_quote": "throbbing headache"
      },
      {
        "name": "Headache Laterality",
        "value": "Unilateral",
        "evidence_quote": "unilateral throbbing headache"
      },
      {
        "name": "Visual Aura",
        "value": "Visual scotomata",
        "evidence_quote": "visual scotomata"
      },
      {
        "name": "Photophobia",
        "value": "Present",
        "evidence_quote": "photophobia"
      },
      {
        "name": "Nausea",
        "value": "Present",
        "evidence_quote": "nausea"
      },
      {
        "name": "Phonophobia",
        "value": "Present",
        "evidence_quote": "phonophobia"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT07402954",
        "title": "Stimulation of External Carotid Artery Circulation",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥18",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 34-year-old woman",
            "reasoning": "Patient age 34 exceeds minimum age requirement of 18"
          },
          {
            "text": "Chronic migraine or status migrainosus, or craniofacial pain refractory to maximal medical therapy who are undergoing MMA IA lidocaine infusion",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia",
            "reasoning": "Clinical presentation consistent with migraine; chronicity, treatment refractoriness, and MMA treatment status undefined"
          },
          {
            "text": "Subject has provided informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette does not address informed consent status"
          },
          {
            "text": "Known allergies to lidocaine",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about lidocaine allergy or drug allergies"
          },
          {
            "text": "Seizure disorder, history of seizures, or increased seizure susceptibility",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No mention of seizure disorder or seizure history"
          },
          {
            "text": "Intracranial vascular malformations or dural AVF",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about intracranial vascular pathology or AVF"
          },
          {
            "text": "Hemodynamic instability, any condition where brief hemodynamic shifts may pose risk",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No hemodynamic or cardiovascular stability information provided"
          },
          {
            "text": "Previous MMA intervention or craniotomy that could result in MMA occlusion",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No surgical history or prior MMA intervention mentioned"
          },
          {
            "text": "Any implanted electronic device (pacemaker, ICD, DBS, VNS, cochlear implant, spinal cord stimulator)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of implanted electronic devices"
          },
          {
            "text": "Significant cardiovascular disease (unstable angina, severe arrhythmias, recent MI)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No cardiovascular disease history provided"
          },
          {
            "text": "Active systemic infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about active systemic infections"
          },
          {
            "text": "Vulnerable populations (pregnant individuals, children, prisoners, individuals lacking decision-making capacity, persons with cognitive impairment, those unable to provide informed consent)",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": "A 34-year-old woman",
            "reasoning": "Adult non-child without apparent cognitive impairment; pregnancy status and formal consent capacity undocumented"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Severe migraines with aura; meets age; refractory-to-therapy status needs clarification for MMA intervention."
      },
      {
        "nct_id": "NCT06785129",
        "title": "Endometriosis and Migraine",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients with diagnosed endometriosis, migraine, or both endometriosis and migraine",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia",
            "reasoning": "Clinical presentation diagnostic for migraine with aura"
          },
          {
            "text": "Healthy control subjects with no history of chronic pain",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "recurrent episodes of severe unilateral throbbing headache",
            "reasoning": "Patient has chronic migraine pain; does not qualify as healthy control"
          },
          {
            "text": "Age 12-45",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "34-year-old woman",
            "reasoning": "Age 34 falls within inclusion range 12-45"
          },
          {
            "text": "Assigned female sex at birth",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 34-year-old woman",
            "reasoning": "Female, consistent with assigned female sex at birth"
          },
          {
            "text": "Pregnancy or breastfeeding",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Pregnancy or breastfeeding status not documented"
          },
          {
            "text": "Presence of prolactinoma",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about prolactinoma history provided"
          },
          {
            "text": "Presence of psychiatric, neurological, endocrinological and/or developmental conditions and taking medications for these conditions",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": "recurrent episodes of severe unilateral throbbing headache",
            "reasoning": "Migraine is neurological condition; current medication status unknown"
          },
          {
            "text": "Current use of dopamine agonist or SSRI medications",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Current dopamine agonist or SSRI use not documented"
          },
          {
            "text": "For patients aged 12-17 not having a parent/legal guardian willing to sign the consent and answer surveys about their child's health",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "34-year-old",
            "reasoning": "Criterion applies only to ages 12-17; patient is outside this range"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Female with migraine, age 12-45; meets patient-cohort inclusion; endometriosis status and parental-consent exclusion unclear."
      },
      {
        "nct_id": "NCT06788977",
        "title": "External Trigeminal Nerve Stimulation for Migraine Treatment in Pregnancy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age between 18-44 years at enrollment",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 34-year-old woman",
            "reasoning": "Patient age 34 falls within 18-44 year range."
          },
          {
            "text": "Pregnant at time of enrollment",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status mentioned in vignette."
          },
          {
            "text": "Singleton pregnancy (one fetus/baby)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status; cannot assess gestation number."
          },
          {
            "text": "Headaches or migraines prior to pregnancy that continued into pregnancy",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status; cannot assess headache timing relative to pregnancy."
          },
          {
            "text": "Headaches or migraines began during first trimester of pregnancy",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status; cannot determine first trimester onset."
          },
          {
            "text": "Able to provide proof of active intrauterine pregnancy and estimated due date via online document upload",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status or documentation capability mentioned."
          },
          {
            "text": "Has access to email, text messages, smartphone or computer with internet access",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about technology access."
          },
          {
            "text": "Willing and able to provide consent for registry participation",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about consent willingness provided."
          },
          {
            "text": "Multigestational pregnancy (more than one fetus/baby)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pregnancy status; cannot assess number of fetuses."
          },
          {
            "text": "Any other condition which might preclude participation in the opinion of the patient's physician(s) or the study's principal investigator",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Requires physician judgment; no medical opinion provided."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 3,
        "rationale": "Age 18-44 fits; migraine history present; pregnancy status unknown but essential inclusion criterion."
      },
      {
        "nct_id": "NCT06995729",
        "title": "A Study to Learn About the Study Medicine Called Zavegepant (PF-07930207) in Children With a History of Migraine",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Participants aged 6 years to less than 12 years",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "34-year-old woman",
            "reasoning": "Patient age 34 exceeds trial maximum of <12 years"
          },
          {
            "text": "Documented medical history of migraine with or without aura for at least 6 months before the Screening Visit",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia",
            "reasoning": "Migraine with aura presentation documented; 6-month duration not confirmed"
          },
          {
            "text": "Weight >15 kg at the Screening Visit",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Weight not provided in patient vignette"
          },
          {
            "text": "Evidence or history of clinically significant disease",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No comorbid clinically significant disease documented"
          },
          {
            "text": "Continuous migraine (defined as an unrelenting headache) within 1 month prior to Screening Visit",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Recurrent episodes",
            "reasoning": "Episodic headaches; no continuous/unrelenting pattern documented"
          },
          {
            "text": "Atypical migraine types, complications of a migraine, or a confounding and clinically significant pain syndrome",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Unilateral throbbing, visual scotomata, photophobia, nausea, phonophobia",
            "reasoning": "Typical migraine with aura presentation; no atypical features mentioned"
          },
          {
            "text": "Conditions that may affect the administration or absorption of the nasal product",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Nasal conditions or absorption impairments not addressed"
          },
          {
            "text": "Clinically significant depression (Promis Parent Proxy SF 2.0 Depressive Scale T score ≥70)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Depression screening scores not provided"
          },
          {
            "text": "Suicidal ideation and behaviour (C-SSRS: any \"yes\" to items 2 to 5 or any \"yes\" to suicide behaviours)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Suicidal risk assessment not documented"
          },
          {
            "text": "Serum Total bilirubin >1.5 × ULN (Upper Limit of Normal), AST (Aspartate Transferase) or ALT (Alanine Transaminase) >2 × ULN",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Laboratory values not provided"
          },
          {
            "text": "Abnormal ECG (Electrocardiogram) at screening visit",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "ECG findings not documented"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Age 34 exceeds pediatric enrollment ceiling (6-12); meets multiple exclusion criteria."
      }
    ],
    "questions": [
      {
        "field": "Cardio-neuro medical history",
        "question": "Do you have any history of heart disease, cardiac arrhythmias, or neurological conditions like stroke or arterial dissection?",
        "why": "MMA procedure carries cardiovascular and neurological risks; affects 6 trial criteria"
      },
      {
        "field": "Pregnancy status and type",
        "question": "Are you currently pregnant, planning pregnancy within the next year, or what form of contraception are you using?",
        "why": "Multiple trials have distinct pregnancy-specific inclusion/exclusion criteria"
      },
      {
        "field": "Current medications and allergies",
        "question": "What medications are you currently taking for migraines and other conditions, and do you have any known drug allergies?",
        "why": "Assess drug interactions and contraindications for trial interventions"
      }
    ],
    "reeval": {
      "extended_record": "Patient denies any history of heart disease, cardiac arrhythmias, or prior neurological events including stroke or arterial dissection. Not currently pregnant, with no plans for pregnancy in the next 12 months; uses a copper IUD (placed 3 years ago) for contraception. For migraine management, she takes sumatriptan 50 mg as needed for acute episodes (4–6 times monthly) and topiramate 50 mg daily for prophylaxis, initiated 18 months ago. Also takes a daily multivitamin. No known drug allergies. Denies tobacco; minimal alcohol use.",
      "answers": [
        {
          "question": "Do you have any history of heart disease, cardiac arrhythmias, or neurological conditions like stroke or arterial dissection?",
          "answer": "No cardiac or neurological disease history reported.",
          "evidence_quote": "Patient denies any history of heart disease, cardiac arrhythmias, or prior neurological events including stroke or arterial dissection."
        },
        {
          "question": "Are you currently pregnant, planning pregnancy within the next year, or what form of contraception are you using?",
          "answer": "Not pregnant, no pregnancy plans in next 12 months; uses copper IUD for contraception.",
          "evidence_quote": "Not currently pregnant, with no plans for pregnancy in the next 12 months; uses a copper IUD (placed 3 years ago) for contraception."
        },
        {
          "question": "What medications are you currently taking for migraines and other conditions, and do you have any known drug allergies?",
          "answer": "Sumatriptan 50 mg for acute migraines and topiramate 50 mg daily for prophylaxis; no known drug allergies.",
          "evidence_quote": "For migraine management, she takes sumatriptan 50 mg as needed for acute episodes (4–6 times monthly) and topiramate 50 mg daily for prophylaxis, initiated 18 months ago. Also takes a daily multivitamin. No known drug allergies."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT07402954",
          "criterion": "Known allergies to lidocaine",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Seizure disorder, history of seizures, or increased seizure susceptibility",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Hemodynamic instability, any condition where brief hemodynamic shifts may pose risk",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Previous MMA intervention or craniotomy that could result in MMA occlusion",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Any implanted electronic device (pacemaker, ICD, DBS, VNS, cochlear implant, spinal cord stimulator)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Significant cardiovascular disease (unstable angina, severe arrhythmias, recent MI)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Vulnerable populations (pregnant individuals, children, prisoners, individuals lacking decision-making capacity, persons with cognitive impairment, those unable to provide informed consent)",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06785129",
          "criterion": "Pregnancy or breastfeeding",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06785129",
          "criterion": "Presence of psychiatric, neurological, endocrinological and/or developmental conditions and taking medications for these conditions",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06785129",
          "criterion": "Current use of dopamine agonist or SSRI medications",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06788977",
          "criterion": "Pregnant at time of enrollment",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06788977",
          "criterion": "Singleton pregnancy (one fetus/baby)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06788977",
          "criterion": "Multigestational pregnancy (more than one fetus/baby)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT07402954",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Classic migraine with aura; age eligible; refractory-to-maximal-medical-therapy status unclear; no confirmed contraindications."
        },
        {
          "nct_id": "NCT06785129",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Migraine documented but excluded: neurological condition on medications (migraine treatment presumed)."
        },
        {
          "nct_id": "NCT06788977",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Not pregnant; trial requires pregnancy inclusions; migraine present but pregnancy status disqualifying."
        },
        {
          "nct_id": "NCT06995729",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Age 34 exceeds pediatric upper limit (6–<12); clinically significant disease and symptom exclusions met."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S006",
    "patient_text": "A 45-year-old man with poorly controlled type 2 diabetes presents with fever, facial pain, black necrotic eschar on the nasal mucosa, and periorbital swelling.",
    "extraction": [
      {
        "name": "Age",
        "value": "45 years old",
        "evidence_quote": "45-year-old"
      },
      {
        "name": "Sex",
        "value": "male",
        "evidence_quote": "man"
      },
      {
        "name": "Past Medical History",
        "value": "poorly controlled type 2 diabetes",
        "evidence_quote": "poorly controlled type 2 diabetes"
      },
      {
        "name": "Chief Complaint",
        "value": "fever, facial pain, black necrotic eschar on nasal mucosa, periorbital swelling",
        "evidence_quote": "presents with fever, facial pain, black necrotic eschar on the nasal mucosa, and periorbital swelling"
      },
      {
        "name": "Symptom",
        "value": "fever",
        "evidence_quote": "fever"
      },
      {
        "name": "Symptom",
        "value": "facial pain",
        "evidence_quote": "facial pain"
      },
      {
        "name": "Physical Exam Finding",
        "value": "black necrotic eschar on the nasal mucosa",
        "evidence_quote": "black necrotic eschar on the nasal mucosa"
      },
      {
        "name": "Physical Exam Finding",
        "value": "periorbital swelling",
        "evidence_quote": "periorbital swelling"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT05406037",
        "title": "Biomarkers for Invasive Mucormycosis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Men and women",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "45-year-old man",
            "reasoning": "Patient is male, satisfies men and women criterion"
          },
          {
            "text": "Age 3 to 64 years old (18 to 64 years old for controls)",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "45-year-old man",
            "reasoning": "Age 45 falls within 3–64 year range"
          },
          {
            "text": "Informed consent obtained; parental authority consent required for children",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about informed consent status"
          },
          {
            "text": "Patient social insured",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about insurance or social security status"
          },
          {
            "text": "For case group: Diagnosis of mucormycosis confirmed by conventional mycology data and/or positive q-PCR and/or anatomopathologic diagnosis with compatible clinical situation",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "fever, facial pain, black necrotic eschar on nasal mucosa, periorbital swelling",
            "reasoning": "Clinical presentation compatible with mucormycosis but no confirmatory mycology, PCR, or pathology mentioned"
          },
          {
            "text": "For control group 1: Patient assessed for hematopoietic stem cell transplantation, at risk for invasive fungal infection, with pre-transplantation review excluding ongoing infection",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about hematopoietic stem cell transplantation assessment"
          },
          {
            "text": "For control group 2: Diagnosis of disseminated candidiasis or invasive pulmonary aspergillosis according to EORTC/MSG criteria or AspICU criteria",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "fever, facial pain, black necrotic eschar on nasal mucosa, periorbital swelling",
            "reasoning": "Clinical presentation indicates mucormycosis, not candidiasis or aspergillosis"
          },
          {
            "text": "Patients for whom the inclusion criteria are not met",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": null,
            "reasoning": "Excludes patients not meeting inclusion criteria; outcome depends on unconfirmed diagnostic status and missing consent/insurance data"
          },
          {
            "text": "Co-infection mucormycosis/other invasive fungal infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about co-infections or other concurrent invasive fungal infections"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Suspected mucormycosis with rhinonasal eschar fits case group; age 45 within 3-64 range; diagnosis confirmation pending."
      },
      {
        "nct_id": "NCT07339800",
        "title": "Chest CT Scan in Pulmonary Mucormycosis: Prognostic Value",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients aged 18 years or older",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "45-year-old man",
            "reasoning": "Patient's age 45 meets minimum inclusion age of 18 years."
          },
          {
            "text": "Treated at Strasbourg University Hospital between January 1, 2009, and June 3, 2025",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about treatment facility or admission dates."
          },
          {
            "text": "With a diagnosis of probable or proven invasive pulmonary infection with Mucorales according to the 2020 EORTC/MSGERC criteria",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "black necrotic eschar on the nasal mucosa, periorbital swelling",
            "reasoning": "Clinical presentation highly suggestive of invasive Mucorales but pulmonary involvement not documented; rhino-cerebral features present only."
          },
          {
            "text": "Having undergone at least one CT scan including the thoracic region",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no information about imaging studies or CT scans."
          },
          {
            "text": "No CT scan including the thoracic region",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about CT imaging status or thoracic imaging studies."
          },
          {
            "text": "No diagnosis of probable or proven invasive pulmonary infection with Mucorales according to the 2020 EORTC/MSGERC criteria",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": null,
            "reasoning": "Vignette documents no formal diagnosis of invasive pulmonary Mucorales; rhino-cerebral presentation only."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Pulmonary-specific trial; patient's rhinocerebral form not pulmonary-focused; treatment location and diagnosis status uncertain."
      },
      {
        "nct_id": "NCT07654647",
        "title": "Clinical Evaluation of Patient-Specific 3D-Printed Titanium Implants for Facial Reconstruction.",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 18 years or older",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "45-year-old man",
            "reasoning": "Patient age exceeds 18-year minimum."
          },
          {
            "text": "Presence of facial bone defects resulting from cystic or tumoral osteolytic lesions",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "black necrotic eschar on the nasal mucosa, periorbital swelling",
            "reasoning": "Acute necrotizing soft tissue infection, not cystic/tumoral osteolytic lesions."
          },
          {
            "text": "Acquired or congenital facial deformities associated with bony defects or facial asymmetry",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "fever, facial pain, black necrotic eschar on the nasal mucosa, periorbital swelling",
            "reasoning": "Acute inflammatory findings without documented chronic bony defects or structural deformity."
          },
          {
            "text": "Patients requiring patient-specific 3D-printed titanium implants for maxillofacial reconstruction",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information regarding implant candidacy or reconstruction needs."
          },
          {
            "text": "Aesthetic indications requiring custom facial implant design, including microgenia (chin retrusion)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No documentation of aesthetic indications or implant design requirements."
          },
          {
            "text": "Ability to provide written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on cognitive status or ability to provide informed consent."
          },
          {
            "text": "Active pathological lesions at the time of enrollment",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "fever, facial pain, black necrotic eschar on the nasal mucosa, periorbital swelling",
            "reasoning": "Multiple active pathological findings present at presentation; exclusion applies."
          },
          {
            "text": "Age below 18 years",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "45-year-old man",
            "reasoning": "Patient is not below 18 years; exclusion does not apply."
          },
          {
            "text": "History of radiotherapy within 12 months prior to enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No radiotherapy history documented in vignette."
          },
          {
            "text": "Chronic untreated vitamin D deficiency",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No vitamin D level or deficiency status reported."
          },
          {
            "text": "Uncontrolled diabetes mellitus",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "poorly controlled type 2 diabetes",
            "reasoning": "Uncontrolled diabetes documented; exclusion applies."
          },
          {
            "text": "Inability or unwillingness to comply with follow-up requirements",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information on compliance capacity or willingness."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Reconstructive implant trial; acute mucormycotic necrosis not within surgical indication; active pathology excludes participation."
      },
      {
        "nct_id": "NCT06440915",
        "title": "Study on Theraputic Drug Monitoring and Phamacokinetics of Isavuconazole in Children",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients who intend to take isavuconazole for the treatment of invasive mycosis",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No explicit statement of treatment intent with isavuconazole documented in vignette."
          },
          {
            "text": "Aged 0-18 years, gender unlimited",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "45-year-old man",
            "reasoning": "Patient is 45 years old; inclusion criterion requires age 0-18 years."
          },
          {
            "text": "Subject and guardian willing to comply with the procedures and operations specified in the study protocol",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided regarding patient's willingness or ability to comply."
          },
          {
            "text": "Guardian and subject (if of independent informed age) willing and able to provide written informed consent to participate in the study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about informed consent status or documentation provided."
          },
          {
            "text": "Known allergy to any azole antifungal therapy or other ingredients contained in the study drug",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No allergy history or drug sensitivities documented in patient information."
          },
          {
            "text": "Any condition of the child that may interfere with study participation or other inappropriate conditions as determined by the researcher",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "poorly controlled type 2 diabetes presents with fever, facial pain, black necrotic eschar on the nasal mucosa, and periorbital swelling",
            "reasoning": "Acute invasive mycosis and uncontrolled diabetes would substantially interfere with study participation."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Pediatric trial (ages 0-18); patient is 45 years old; fails primary age inclusion criterion."
      }
    ],
    "questions": [
      {
        "field": "informed_consent_and_legal_capacity",
        "question": "Has the patient provided written informed consent to participate in this trial, or does he require a legal guardian/proxy to provide consent?",
        "why": "4 trial criteria require documented informed consent; essential gating criterion"
      },
      {
        "field": "microbiological_imaging_confirmation_of_invasive_mycosis",
        "question": "Has a tissue biopsy or imaging (CT/MRI) confirmed mucormycosis, or is this based on clinical suspicion only?",
        "why": "3 trials require confirmed diagnosis; clinical presentation insufficient alone"
      },
      {
        "field": "treatment_compliance_and_follow_up_willingness",
        "question": "Can the patient commit to frequent follow-up visits and sustained antifungal therapy as required by trial protocols?",
        "why": "Affects ability to complete 2+ trials; non-compliance is primary dropout risk"
      }
    ],
    "reeval": {
      "extended_record": "Patient provided written informed consent on admission after formal capacity assessment. Nasal endoscopy with biopsy revealed broad, non-septate hyphae consistent with Mucorales on histology; GMS stain positive. CT orbits and sinuses showed maxillary and ethmoid sinus opacification with extension into left orbital apex and periorbital tissues, measuring 7 mm edema. Bone erosion of medial orbital wall evident. HbA1c 12.3%, blood glucose 298 mg/dL. Laboratory workup: ESR 58 mm/h, WBC 13,800/μL, creatinine 1.0 mg/dL, albumin 3.2 g/dL. Patient lives within 3 miles of medical center and confirmed employment flexibility for intensive follow-up. Committed to twice-weekly clinic visits, daily amphotericin B infusions initially, and oral posaconazole continuation therapy. No contraindications to trial participation identified on review.",
      "answers": [
        {
          "question": "Has the patient provided written informed consent to participate in this trial, or does he require a legal guardian/proxy to provide consent?",
          "answer": "Patient provided written informed consent after capacity assessment; no proxy required.",
          "evidence_quote": "Patient provided written informed consent on admission after formal capacity assessment."
        },
        {
          "question": "Has a tissue biopsy or imaging (CT/MRI) confirmed mucormycosis, or is this based on clinical suspicion only?",
          "answer": "Confirmed by nasal tissue biopsy showing broad non-septate hyphae consistent with Mucorales (GMS stain positive) and CT imaging showing sinus involvement with orbital extension.",
          "evidence_quote": "Nasal endoscopy with biopsy revealed broad, non-septate hyphae consistent with Mucorales on histology; GMS stain positive. CT orbits and sinuses showed maxillary and ethmoid sinus opacification with extension into left orbital apex"
        },
        {
          "question": "Can the patient commit to frequent follow-up visits and sustained antifungal therapy as required by trial protocols?",
          "answer": "Yes. Patient lives within 3 miles of treatment center with confirmed employment flexibility and has committed to twice-weekly clinic visits and sustained antifungal therapy.",
          "evidence_quote": "Patient lives within 3 miles of medical center and confirmed employment flexibility for intensive follow-up. Committed to twice-weekly clinic visits, daily amphotericin B infusions initially, and oral posaconazole continuation therapy."
        }
      ],
      "verdict_changes": [],
      "final_ranking": [
        {
          "nct_id": "NCT05406037",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Suspected mucormycosis with rhinonasal eschar fits case group; age 45 within 3-64 range; diagnosis confirmation pending."
        },
        {
          "nct_id": "NCT07339800",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Pulmonary-specific trial; patient's rhinocerebral form not pulmonary-focused; treatment location and diagnosis status uncertain."
        },
        {
          "nct_id": "NCT07654647",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Reconstructive implant trial; acute mucormycotic necrosis not within surgical indication; active pathology excludes participation."
        },
        {
          "nct_id": "NCT06440915",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Pediatric trial (ages 0-18); patient is 45 years old; fails primary age inclusion criterion."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S007",
    "patient_text": "A 3-month-old infant with projectile non-bilious vomiting after feeding, visible peristalsis, and a palpable olive-shaped mass in the epigastrium. Labs show hypochloremic, hypokalemic metabolic alkalosis.",
    "extraction": [
      {
        "name": "Age",
        "value": "3 months",
        "evidence_quote": "3-month-old"
      },
      {
        "name": "Patient type",
        "value": "Infant",
        "evidence_quote": "infant"
      },
      {
        "name": "Vomiting character",
        "value": "Projectile, non-bilious",
        "evidence_quote": "projectile non-bilious vomiting"
      },
      {
        "name": "Vomiting trigger",
        "value": "After feeding",
        "evidence_quote": "after feeding"
      },
      {
        "name": "Visible peristalsis",
        "value": "Present",
        "evidence_quote": "visible peristalsis"
      },
      {
        "name": "Epigastric mass",
        "value": "Palpable, olive-shaped",
        "evidence_quote": "palpable olive-shaped mass in the epigastrium"
      },
      {
        "name": "Serum chloride",
        "value": "Low",
        "evidence_quote": "hypochloremic"
      },
      {
        "name": "Serum potassium",
        "value": "Low",
        "evidence_quote": "hypokalemic"
      },
      {
        "name": "Acid-base disturbance",
        "value": "Metabolic alkalosis",
        "evidence_quote": "metabolic alkalosis"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06031025",
        "title": "Prevalence and Natural History of Functional Gastrointestinal Disorders Among At-risk Infants.",
        "phase": "NA",
        "criteria": [
          {
            "text": "infants with gestational age at birth < 31 weeks",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No gestational age at birth documented"
          },
          {
            "text": "infants with gestational age at birth < 37 weeks and major respiratory or neurologic morbidity",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No gestational age or major respiratory/neurologic morbidity data"
          },
          {
            "text": "infants with history of perinatal asphyxia",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No perinatal asphyxia history documented"
          },
          {
            "text": "lack of informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Informed consent status not addressed"
          },
          {
            "text": "diagnosis of congenital or other major gastrointestinal disease (i.e. inflammatory bowel disease, cancer)",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "palpable olive-shaped mass in the epigastrium, projectile non-bilious vomiting, visible peristalsis, hypochloremic hypokalemic metabolic alkalosis",
            "reasoning": "Clinical findings diagnostic of pyloric stenosis, a major congenital GI disease"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "At-risk infants study; prematurity status and risk factor history unknown; no clear exclusions identified."
      },
      {
        "nct_id": "NCT05535361",
        "title": "A Feasibility Study to Evaluate Safety and Probable Benefit of the Eclipse XL1 System for Distraction Enterogenesis in Adult and Pediatric Patients With Short Bowel Syndrome",
        "phase": "NA",
        "criteria": [
          {
            "text": "Subject has short bowel syndrome, defined as 50% or less of expected bowel length based on subject age and/or height, and measured at the time of the subject's prior intestinal resection.",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "palpable olive-shaped mass in the epigastrium",
            "reasoning": "Olive mass indicates pyloric stenosis, not short bowel syndrome or prior resection."
          },
          {
            "text": "Minimum residual bowel length of 3 cm.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette lacks bowel length measurements needed to assess this criterion."
          },
          {
            "text": "Male or female patients aged 3 months to 65 years inclusive.",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "3-month-old infant",
            "reasoning": "Patient age 3 months falls within stated inclusion range."
          },
          {
            "text": "The subject, parent or legal guardian is able to read, understand, and is willing to provide informed consent.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette does not address parental informed consent capability."
          },
          {
            "text": "The subject or parent or legal guardian is able to understand the requirements of the study and is willing to bring the subject to all clinic visits and complete all study related procedures.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette does not address study compliance willingness."
          },
          {
            "text": "Ultra-short bowel syndrome defined as less than 3 cm of bowel length.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No bowel length measurement provided; presentation consistent with pyloric stenosis."
          },
          {
            "text": "Diagnosed Inflammatory bowel disease-unclassified (not Crohn's or ulcerative colitis).",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "non-bilious vomiting",
            "reasoning": "Non-bilious vomiting and epigastric mass indicate pyloric stenosis, not inflammatory IBD-U."
          },
          {
            "text": "Evidence of active or prior Crohn's disease.",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "non-bilious vomiting",
            "reasoning": "Non-bilious vomiting, olive mass suggest pyloric stenosis, not Crohn's disease."
          },
          {
            "text": "Primary intestinal failure (without loss or resection of intestinal tissue).",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "palpable olive-shaped mass in the epigastrium",
            "reasoning": "Hypertrophied pyloric muscle with mechanical obstruction, not primary intestinal failure."
          },
          {
            "text": "Coagulopathy, as defined by INR > 1.4 or platelets < 100.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "INR and platelet values not documented in vignette."
          },
          {
            "text": "Known immunocompromised status including organ transplantation, chemotherapy or radiotherapy within the past 12 months, clinically significant leukopenia, HIV positive, or immune status making the subject a poor candidate in the opinion of the Investigator.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No transplant, chemotherapy, radiotherapy, or immunocompromised status documented."
          },
          {
            "text": "Subject is determined by the investigator to be unsuitable for participation in this trial for any reason.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Investigator suitability assessment cannot be determined from clinical vignette."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Age-eligible (3 months within 3mo-65yr range) but lacks short bowel syndrome; primary inclusion criterion not met."
      },
      {
        "nct_id": "NCT06687564",
        "title": "Role of ACTG2 Variants in Smooth Muscle Determination and Function in Pediatric Intestinal Pseudo-obstruction.",
        "phase": "NA",
        "criteria": [
          {
            "text": "Minor or adult patient ≥ 4 years of age",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Age: 3 months",
            "reasoning": "Patient 3 months old; criterion requires ≥4 years"
          },
          {
            "text": "Patient with PIPO before age 18",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Projectile non-bilious vomiting after feeding, visible peristalsis, and a palpable olive-shaped mass in the epigastrium",
            "reasoning": "Clinical presentation classic for pyloric stenosis, not PIPO"
          },
          {
            "text": "Patient with PIPO meeting at least 2 of the ESPGHAN criteria (Thapar et al 2018) and carrying the R178, R257, R40 or A136 mutation of the ACTG2 gene",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Palpable olive-shaped mass; projectile non-bilious vomiting",
            "reasoning": "Clinical features consistent with pyloric stenosis, not PIPO diagnosis"
          },
          {
            "text": "Patient whose assent has been obtained and whose legal guardians have given their written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette contains no information regarding consent status"
          },
          {
            "text": "Patient affiliated to the French Social Security system or benefiting from an equivalent plan",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about French Social Security affiliation provided"
          },
          {
            "text": "iPS cell lines MS573 or WT8288 or 202CT or SD378M, from the Nantes University Hospital biological collection and generated from samples from control patients without POIC who have consented to donate their samples",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about iPS cell lines or biological samples mentioned"
          },
          {
            "text": "Patients with a history of radiotherapy treatment",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Age: 3 months",
            "reasoning": "No radiotherapy history documented; exclusion criterion satisfied"
          },
          {
            "text": "Patient with lymphocyte lineage damage",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about lymphocyte function or damage"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Requires PIPO diagnosis and ACTG2 mutations; patient 3 months old (≥4yr required); exclusion criterion met (radiotherapy)."
      },
      {
        "nct_id": "NCT04515251",
        "title": "Ultrasound Evaluation of Superior Mesenteric Artery Measurements in a Healthy Pediatric Population",
        "phase": "NA",
        "criteria": [
          {
            "text": "Male and female children",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Patient type: Infant",
            "reasoning": "Patient is a child, but sex not documented in vignette."
          },
          {
            "text": "Age ranging from 10 to 15 years, included",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Age: 3 months",
            "reasoning": "Patient is 3 months old; trial requires 10-15 years."
          },
          {
            "text": "Abdominal ultrasound examination to be performed for indications other than gastrointestinal evaluation",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Projectile non-bilious vomiting after feeding, visible peristalsis, palpable olive-shaped mass in the epigastrium",
            "reasoning": "Patient has GI condition (pyloric stenosis); ultrasound would be for GI evaluation."
          },
          {
            "text": "Signed Informed Consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about informed consent status in vignette."
          },
          {
            "text": "Presence of a disease that could distort the anatomy around the SMA (e.g., abdominal mass, lymphadenopathy, severe scoliosis, free abdominal fluid)",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "Palpable olive-shaped mass in the epigastrium",
            "reasoning": "Patient has abdominal mass; exclusion criterion is triggered."
          },
          {
            "text": "Oncologic patients at risk of neoplastic cachexia",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "A 3-month-old infant with projectile non-bilious vomiting after feeding, visible peristalsis, and a palpable olive-shaped mass",
            "reasoning": "Patient has pyloric stenosis, not oncologic disease; exclusion criterion not applicable."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Requires age 10–15 years and non-GI ultrasound indication; patient 3 months old with GI pathology."
      }
    ],
    "questions": [
      {
        "field": "Informed consent status",
        "question": "Have parents signed informed consent for this clinical trial?",
        "why": "Required for legal trial participation (affects 5 criteria)"
      },
      {
        "field": "Gestational age and perinatal complications",
        "question": "What was gestational age at birth? Any prematurity or delivery complications?",
        "why": "Determines preterm/asphyxia-related exclusion criteria (affects 3)"
      },
      {
        "field": "Residual bowel length measurement",
        "question": "Has bowel length been measured on imaging or surgical exploration?",
        "why": "Defines ultra-short bowel syndrome eligibility (affects 2)"
      }
    ],
    "reeval": {
      "extended_record": "Patient S007 is a 3-month-old male who presented with classic pyloric stenosis symptoms. Parents provided informed written consent for trial enrollment on admission. Maternal history reveals term gestation at 39 weeks with spontaneous vaginal delivery without complications; birth weight 3.4 kg. Prenatal course was unremarkable. On abdominal ultrasound, pyloric muscle thickness measured 4.2 mm with pyloric channel length of 17 mm, confirming IHPS diagnosis. Pyloromyotomy performed via laparoscopic approach with uncomplicated intraoperative course. Intraoperative findings documented normal small bowel anatomy with total measured bowel length of 485 cm from pylorus to ileocecal valve. Post-operative electrolyte repletion corrected the metabolic alkalosis (pH 7.52 → 7.41, chloride 88 → 104 mEq/L, potassium 2.9 → 4.1 mEq/L). Feeding resumed on post-operative day 2 with good tolerance.",
      "answers": [
        {
          "question": "Have parents signed informed consent for this clinical trial?",
          "answer": "Yes, informed written consent was obtained on admission",
          "evidence_quote": "Parents provided informed written consent for trial enrollment on admission."
        },
        {
          "question": "What was gestational age at birth? Any prematurity or delivery complications?",
          "answer": "Term gestation at 39 weeks via spontaneous vaginal delivery without complications",
          "evidence_quote": "term gestation at 39 weeks with spontaneous vaginal delivery without complications"
        },
        {
          "question": "Has bowel length been measured on imaging or surgical exploration?",
          "answer": "Yes, measured intraoperatively at 485 cm from pylorus to ileocecal valve",
          "evidence_quote": "total measured bowel length of 485 cm from pylorus to ileocecal valve"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06031025",
          "criterion": "infants with gestational age at birth < 31 weeks",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "infants with gestational age at birth < 37 weeks and major respiratory or neurologic morbidity",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "infants with history of perinatal asphyxia",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "lack of informed consent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06687564",
          "criterion": "Patient whose assent has been obtained and whose legal guardians have given their written informed consent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT04515251",
          "criterion": "Signed Informed Consent",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06031025",
          "rank": 1,
          "eligibility": "INELIGIBLE",
          "rationale": "3-month-old term infant lacking at-risk features (prematurity, asphyxia, GA<37w). Pyloric stenosis is structural, not functional GI disorder."
        },
        {
          "nct_id": "NCT05535361",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Age-eligible (3mo–65y) but primary inclusion short bowel syndrome NOT_MET. Patient has pyloric stenosis, not SBS."
        },
        {
          "nct_id": "NCT06687564",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Age inclusion NOT_MET (≥4y). PIPO diagnosis NOT_MET. Patient has pyloric stenosis, not pseudo-obstruction."
        },
        {
          "nct_id": "NCT04515251",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Age NOT_MET (10–15y; patient 3mo). Designed for healthy ultrasound controls; patient has acute surgical GI pathology."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S008",
    "patient_text": "A 60-year-old woman presents with progressive dyspnea, dry cough, and clubbing of the fingers. Chest CT reveals bilateral basal reticular opacities with honeycombing.",
    "extraction": [
      {
        "name": "Age",
        "value": "60 years old",
        "evidence_quote": "60-year-old"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "woman"
      },
      {
        "name": "Presenting Symptom 1",
        "value": "Progressive dyspnea",
        "evidence_quote": "progressive dyspnea"
      },
      {
        "name": "Presenting Symptom 2",
        "value": "Dry cough",
        "evidence_quote": "dry cough"
      },
      {
        "name": "Physical Examination Finding",
        "value": "Clubbing of the fingers",
        "evidence_quote": "clubbing of the fingers"
      },
      {
        "name": "Imaging Modality",
        "value": "Chest CT",
        "evidence_quote": "Chest CT"
      },
      {
        "name": "Imaging Finding 1",
        "value": "Bilateral basal reticular opacities",
        "evidence_quote": "bilateral basal reticular opacities"
      },
      {
        "name": "Imaging Finding 2",
        "value": "Honeycombing",
        "evidence_quote": "honeycombing"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT07447102",
        "title": "Phase II Clinical Study of BC006 in Patients With Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE2",
        "criteria": [
          {
            "text": "Diagnosis of idiopathic pulmonary fibrosis (IPF) according to the 2022 American Thoracic Society/European Respiratory Society/Japanese Respiratory Society/Latin American Thoracic Society (ATS/ERS/JRS/ALAT) clinical practice guideline",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Progressive dyspnea, dry cough, clubbing, bilateral basal reticular opacities with honeycombing",
            "reasoning": "Clinical and imaging findings highly suggestive of IPF, but formal diagnostic confirmation per 2022 guideline not explicitly stated."
          },
          {
            "text": "HRCT pattern consistent with usual interstitial pneumonia (UIP) or probable UIP for IPF confirmed by independent central imaging review, or if HRCT shows indeterminate UIP, diagnosis of IPF confirmed by histopathology from prior lung biopsy (surgical, video-assisted thoracoscopic, or bronchoscopic cryobiopsy)",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Bilateral basal reticular opacities with honeycombing on Chest CT",
            "reasoning": "Imaging findings consistent with UIP pattern, but independent central imaging review confirmation not documented."
          },
          {
            "text": "Forced vital capacity percent predicted (FVC% predicted) ≥45% during the screening period",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No pulmonary function testing data or FVC measurement provided in vignette."
          },
          {
            "text": "Diffusing capacity of the lung for carbon monoxide percent predicted (DLCO% predicted), corrected for hemoglobin, ≥30% and ≤90% during the screening period",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No DLCO or pulmonary function testing data provided in vignette."
          },
          {
            "text": "Stable dose of nintedanib ≥100 mg BID or pirfenidone ≥400 mg TID for at least 8 weeks prior to screening and during screening, or no nintedanib or pirfenidone for at least 4 weeks prior to screening with no plans to initiate or re-initiate during the study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about current or prior antifibrotic therapy (nintedanib or pirfenidone) documented."
          },
          {
            "text": "Emphysema ≥50%, or emphysema greater than fibrosis, as determined by independent central imaging review of HRCT",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Bilateral basal reticular opacities with honeycombing; no emphysema mentioned",
            "reasoning": "Imaging description emphasizes IPF pattern; no emphysema identified, but quantification not explicitly stated."
          },
          {
            "text": "Acute exacerbation of IPF within 3 months prior to screening or during the screening period, as judged by the investigator",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "Progressive dyspnea and dry cough",
            "reasoning": "Progressive symptoms indicate chronic disease course, not acute exacerbation within 3 months."
          },
          {
            "text": "History of smoking within 3 months prior to screening or during the screening period, or inability to refrain from smoking (including cigarettes, cigars, pipes, and e-cigarettes) for the duration of the study",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No smoking history or current smoking status mentioned in vignette."
          },
          {
            "text": "History of severe cardiovascular or cerebrovascular disease, including but not limited to: ventricular arrhythmia requiring clinical intervention; uncontrolled atrial arrhythmia; congestive heart failure NYHA Class ≥III; LVEF <35%; uncontrolled hypertension (systolic ≥160 mmHg or diastolic ≥100 mmHg); or acute coronary syndrome, stroke, or transient ischemic attack within 6 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No cardiovascular or cerebrovascular symptoms, findings, or medical history documented."
          },
          {
            "text": "Current or suspected malignancy, or history of malignancy within 5 years prior to screening (excluding basal cell carcinoma, squamous cell carcinoma of the skin, superficial bladder cancer, carcinoma in situ of the cervix, or other carcinoma in situ with curative treatment and no recurrence)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No malignancy history or current malignancy status provided in vignette."
          },
          {
            "text": "Active hepatitis B (positive hepatitis B surface antigen and HBV DNA >upper limit of normal) or active hepatitis C (positive hepatitis C antibody and HCV RNA >upper limit of normal)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No hepatitis serology or hepatitis history information provided."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "IPF imaging consistent with UIP pattern (basal honeycombing); no recent acute exacerbation. Diagnosis meets clinical/radiologic features; missing FVC% predicted, DLCO%, and medication regimen."
      },
      {
        "nct_id": "NCT05674994",
        "title": "Glucocorticoids Versus Placebo for the Treatment of Acute Exacerbation of Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Patient is ≥ 18 years of age",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 60-year-old woman",
            "reasoning": "Patient is 60 years old, clearly ≥18 years of age."
          },
          {
            "text": "IPF or IPF (likely) diagnosis defined on 2018 international recommendations",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Bilateral basal reticular opacities with honeycombing",
            "reasoning": "Imaging highly suggestive of IPF/UIP pattern per 2018 criteria but formal diagnosis not explicitly documented."
          },
          {
            "text": "Definite or suspected Acute Exacerbation defined by the international working group criteria after exclusion of alternative diagnoses of acute worsening",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Progressive dyspnea, dry cough",
            "reasoning": "Progressive symptoms indicate chronic disease course, not acute exacerbation; no acute worsening documented."
          },
          {
            "text": "For women of childbearing age: efficient contraception for the duration of the study",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "60-year-old woman",
            "reasoning": "Patient is 60 years old, post-menopausal; not of childbearing age, criterion does not apply."
          },
          {
            "text": "Identified etiology for acute worsening (i.e.: infectious disease)",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No identified etiology or infectious disease documented; patient does not meet exclusion."
          },
          {
            "text": "Known hypersensitivity to glucocorticoids or to any component of the study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about drug hypersensitivity or allergies to glucocorticoids documented."
          },
          {
            "text": "Patient requiring mechanical ventilation or already on mechanical ventilation",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about mechanical ventilation status or current respiratory support."
          },
          {
            "text": "Active bacterial, viral, fungal or parasitic infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about active bacterial, viral, fungal, or parasitic infection."
          },
          {
            "text": "Active cancer",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about active cancer or cancer history documented."
          },
          {
            "text": "Treatment with glucocorticoids > 1 mg/kg/d from more than 7 days in the last 15 days",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about recent glucocorticoid treatment or dosage in past 15 days."
          },
          {
            "text": "Documented pregnancy or lactation",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "60-year-old woman",
            "reasoning": "Patient is 60 years old, post-menopausal; pregnancy and lactation clearly not applicable."
          },
          {
            "text": "Patient on a lung transplantation waiting list",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about lung transplantation waiting list status documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Requires definite/suspected acute exacerbation of IPF. Patient presents with chronic progressive dyspnea and clubbing, not acute worsening."
      },
      {
        "nct_id": "NCT07299695",
        "title": "Intravenous Immunoglobulin for the Treatment of Acute Exacerbations of Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Patients ≥ 18 years of age",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Age 60 exceeds minimum threshold of 18 years."
          },
          {
            "text": "Patients with IPF diagnosis that fulfils ATS/ERS Consensus Criteria",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Bilateral basal reticular opacities with honeycombing",
            "reasoning": "Imaging consistent with IPF but no explicit ATS/ERS confirmed diagnosis documented."
          },
          {
            "text": "Patients hospitalised with a definite or suspected AE-IPF diagnosis, as defined by the international working group criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Vignette describes progressive chronic symptoms but contains no acute exacerbation or hospitalization data."
          },
          {
            "text": "Patient able to understand and sign a written informed consent form, or written informed consent form signed by the patients' legally authorized representative",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about consent capacity or cognitive status."
          },
          {
            "text": "Patients with acute worsening due to uncontrolled heart failure or pulmonary embolism",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No documented heart failure or pulmonary embolism mentioned."
          },
          {
            "text": "Patients with known hypersensitivity to corticosteroids, IVIG or any component of the study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No allergy or hypersensitivity information documented."
          },
          {
            "text": "Patients with known IgA deficiency (IgA level <7 mg/dL)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No IgA level data provided."
          },
          {
            "text": "Patients without a definite diagnosis of IPF or AE-IPF based on clinical, radiological, laboratory evaluation, and multidisciplinary discussion",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": null,
            "reasoning": "Definite IPF diagnosis not explicitly documented; only suggestive clinical/imaging findings present."
          },
          {
            "text": "Patients with active malignancy or currently receiving cancer treatment, except for basal cell or squamous cell skin cancer or low-risk prostate cancer (T1 or T2a stage with PSA <10 ng/dL)",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No documented active malignancy or cancer treatment."
          },
          {
            "text": "Patients that have received treatment for >14 days within the preceding month with >20mg daily prednisone (or equivalent) or any treatment during the last month with immunosuppressants (e.g., cyclophosphamide, mycophenolate)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior treatment or medication history documented."
          },
          {
            "text": "Patients participating in another interventional clinical trial",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided regarding other clinical trial enrollment."
          },
          {
            "text": "Patients with documented pregnancy or lactation",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Age 60 makes pregnancy/lactation highly unlikely; none documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Requires hospitalization with AE-IPF and definite diagnosis by multidisciplinary discussion. Patient has chronic IPF without acute exacerbation; diagnosis UNCERTAIN."
      },
      {
        "nct_id": "NCT03297775",
        "title": "Rheumatoid Arthritis Patients at Risk for Interstitial Lung Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "≥ 45 years old",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Patient age 60 exceeds the 45-year minimum threshold."
          },
          {
            "text": "Diagnosis of RA using the 2010 American College of Rheumatology (ACR) criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No RA diagnosis or ACR criteria assessment documented in vignette."
          },
          {
            "text": "Inability to give informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about patient's consent capacity or cognitive status."
          },
          {
            "text": "Pregnant women",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Patient is clearly not pregnant at age 60."
          },
          {
            "text": "History of interstitial lung disease",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "Bilateral basal reticular opacities with honeycombing",
            "reasoning": "Imaging findings diagnostic of interstitial lung disease; exclusion criterion applies."
          },
          {
            "text": "Evidence of other causes of diffuse parenchymal lung disease such as infection, drug toxicity, other autoimmune processes, etc.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No workup data on infection, drug toxicity, or other autoimmune processes."
          },
          {
            "text": "Over the age of 90 years old",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Patient is 60, well below the 90-year upper age limit."
          },
          {
            "text": "Less than 45 years old",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "60 years old",
            "reasoning": "Patient is 60, exceeds the 45-year lower age exclusion."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Trial designed for RA patients at risk for developing ILD; excludes established interstitial lung disease. Patient has no documented RA and established IPF."
      }
    ],
    "questions": [
      {
        "field": "IPF diagnosis confirmation",
        "question": "Has IPF been confirmed with high-resolution CT and/or histology showing UIP pattern, and have alternative diagnoses been excluded?",
        "why": "Confirms disease; affects 4 trial eligibility criteria"
      },
      {
        "field": "Recent corticosteroid and immunosuppressant use",
        "question": "Has the patient received high-dose corticosteroids or immunosuppressants in the past 3-6 months?",
        "why": "Many trials exclude recent therapy; critical eligibility factor"
      },
      {
        "field": "Pulmonary function tests (FVC% and DLCO%)",
        "question": "What are the most recent FVC and DLCO percentages of predicted?",
        "why": "Determines disease severity and trial-specific eligibility thresholds"
      }
    ],
    "reeval": {
      "extended_record": "HRCT chest with contrast performed 2 months ago showed bilateral basal-predominant reticular opacities with honeycombing pattern consistent with usual interstitial pneumonia (UIP). Transbronchial cryobiopsy obtained during bronchoscopy confirmed UIP pattern with fibroblastic foci and architectural remodeling. Extensive serologic workup performed including ANA, rheumatoid factor, anti-CCP, and anti-GBM antibodies—all negative, effectively excluding connective tissue disease, ANCA vasculitis, and other secondary causes. Pulmonary function tests from 6 weeks ago: FVC 72% of predicted, DLCO 48% of predicted with reduced diffusion capacity disproportionate to ventilatory impairment. Patient has not received high-dose corticosteroids in the past 6 months; instead, initiated on nintedanib 150 mg twice daily 4 months ago for antifibrotic therapy. Continues supplemental oxygen (2 L/min at rest, 3 L/min with exertion).",
      "answers": [
        {
          "question": "Has IPF been confirmed with high-resolution CT and/or histology showing UIP pattern, and have alternative diagnoses been excluded?",
          "answer": "Yes. HRCT demonstrates UIP pattern with honeycombing; transbronchial cryobiopsy histologically confirmed UIP. Comprehensive serologies negative, excluding connective tissue disease and other secondary causes.",
          "evidence_quote": "HRCT chest with contrast performed 2 months ago showed bilateral basal-predominant reticular opacities with honeycombing pattern consistent with usual interstitial pneumonia (UIP). Transbronchial cryobiopsy obtained during bronchoscopy confirmed UIP pattern with fibroblastic foci and architectural remodeling. Extensive serologic workup performed including ANA, rheumatoid factor, anti-CCP, and anti-GBM antibodies—all negative, effectively excluding connective tissue disease, ANCA vasculitis, and other secondary causes."
        },
        {
          "question": "Has the patient received high-dose corticosteroids or immunosuppressants in the past 3-6 months?",
          "answer": "No. Patient initiated on nintedanib (antifibrotic agent) 4 months ago and has not received high-dose corticosteroids.",
          "evidence_quote": "Patient has not received high-dose corticosteroids in the past 6 months; instead, initiated on nintedanib 150 mg twice daily 4 months ago for antifibrotic therapy."
        },
        {
          "question": "What are the most recent FVC and DLCO percentages of predicted?",
          "answer": "FVC 72% predicted; DLCO 48% predicted (measured 6 weeks ago).",
          "evidence_quote": "Pulmonary function tests from 6 weeks ago: FVC 72% of predicted, DLCO 48% of predicted"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT07447102",
          "criterion": "Forced vital capacity percent predicted (FVC% predicted) ≥45% during the screening period",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07447102",
          "criterion": "Diffusing capacity of the lung for carbon monoxide percent predicted (DLCO% predicted), corrected for hemoglobin, ≥30% and ≤90% during the screening period",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05674994",
          "criterion": "IPF or IPF (likely) diagnosis defined on 2018 international recommendations",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05674994",
          "criterion": "Treatment with glucocorticoids > 1 mg/kg/d from more than 7 days in the last 15 days",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07299695",
          "criterion": "Patients with IPF diagnosis that fulfils ATS/ERS Consensus Criteria",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07299695",
          "criterion": "Patients that have received treatment for >14 days within the preceding month with >20mg daily prednisone (or equivalent) or any treatment during the last month with immunosuppressants (e.g., cyclophosphamide, mycophenolate)",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT07447102",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Honeycombing, basal reticular opacities, clubbing consistent with IPF/UIP; lung function met; formal diagnosis confirmation needed"
        },
        {
          "nct_id": "NCT03297775",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "No documented RA diagnosis; trial requires RA enrollment; ILD relevance contingent on RA status"
        },
        {
          "nct_id": "NCT05674994",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Patient has chronic progressive IPF, not acute exacerbation; trial enrollment requires documented acute worsening"
        },
        {
          "nct_id": "NCT07299695",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Acute exacerbation-specific trial; patient has chronic stable disease; multiple exclusion criteria met"
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S009",
    "patient_text": "A 19-year-old male presents with fever, sore throat, fatigue, and posterior cervical lymphadenopathy. Physical exam reveals splenomegaly, and a monospot test is positive.",
    "extraction": [
      {
        "name": "Age",
        "value": "19 years old",
        "evidence_quote": "19-year-old"
      },
      {
        "name": "Sex",
        "value": "male",
        "evidence_quote": "male"
      },
      {
        "name": "Fever",
        "value": "present",
        "evidence_quote": "fever"
      },
      {
        "name": "Sore throat",
        "value": "present",
        "evidence_quote": "sore throat"
      },
      {
        "name": "Fatigue",
        "value": "present",
        "evidence_quote": "fatigue"
      },
      {
        "name": "Posterior cervical lymphadenopathy",
        "value": "present",
        "evidence_quote": "posterior cervical lymphadenopathy"
      },
      {
        "name": "Splenomegaly",
        "value": "present",
        "evidence_quote": "splenomegaly"
      },
      {
        "name": "Monospot test",
        "value": "positive",
        "evidence_quote": "monospot test is positive"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT05127980",
        "title": "Occurrence of Antibodies Cross-reacting With Autoantigens in Primary EBV Infection",
        "phase": "NA",
        "criteria": [
          {
            "text": "Informed consent as documented by signature",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about informed consent documentation in vignette"
          },
          {
            "text": "Confirmed primary EBV infection with compatible clinical presentation including malaise, headache, fever, tonsillitis, pharyngitis, or cervical lymph node enlargement",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "fever, sore throat, fatigue, posterior cervical lymphadenopathy; monospot test positive",
            "reasoning": "EBV confirmed by monospot; fever, pharyngitis, cervical lymphadenopathy, malaise all present"
          },
          {
            "text": "Compatible laboratory picture with lymphocyte count elevation, LUC cells, reactive lymphocytes in manual differential, or elevated liver enzymes",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No CBC, LUC cells, reactive lymphocytes, or liver enzymes reported"
          },
          {
            "text": "Serology compatible with primary EBV infection: anti-EBNA IgG negative, anti-VCA IgG negative, anti-VCA IgM positive",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Specific EBV serology (anti-EBNA, anti-VCA IgG/IgM) not provided; only monospot given"
          },
          {
            "text": "Serology compatible with primary EBV infection: anti-EBNA IgG negative, anti-VCA IgG positive, anti-VCA IgM positive",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Specific EBV serology (anti-EBNA, anti-VCA IgG/IgM) not provided; only monospot given"
          },
          {
            "text": "Clinical picture of upper respiratory tract infection including tonsillitis, pharyngitis, malaise, headache, cough, rhinitis, or cervical node enlargement",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "sore throat, fatigue, posterior cervical lymphadenopathy",
            "reasoning": "Pharyngitis, malaise, and cervical node enlargement present; satisfies upper respiratory criteria"
          },
          {
            "text": "Confirmed primary Cytomegalovirus (CMV) infection",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No CMV serology or testing mentioned; only EBV confirmed"
          },
          {
            "text": "Suspicion or diagnosis of infectious mononucleosis as per judgment of treating clinician",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "monospot test is positive",
            "reasoning": "Confirmed infectious mononucleosis diagnosis by positive monospot and classic presentation"
          },
          {
            "text": "Primary or secondary immunodeficiency",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No immunological workup or immunodeficiency history provided"
          },
          {
            "text": "Treatment with immunosuppressive medication including ≥10mg prednisone equivalent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No medications or immunosuppressive therapy documented"
          },
          {
            "text": "History of autoimmune disease such as systemic lupus erythematosus or vasculitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No past medical history of autoimmune disease mentioned"
          }
        ],
        "eligibility": "ELIGIBLE",
        "rank": 1,
        "rationale": "Confirmed primary EBV with fever, pharyngitis, cervical lymphadenopathy, splenomegaly; no exclusions met."
      },
      {
        "nct_id": "NCT00032513",
        "title": "Genetic Studies of Chronic Active Epstein-Barr Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 1 year old and above",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "19-year-old male",
            "reasoning": "Patient is 19 years old, which exceeds minimum age requirement of 1 year"
          },
          {
            "text": "Severe progressive illness that began as a primary EBV infection, or associated with positive EBV-specific antibody titers (IgG-VCA, ; EA or EBNA) not otherwise explained",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "Monospot test is positive",
            "reasoning": "Positive monospot confirms EBV; specific IgG-VCA or EA titers and severity progression not documented"
          },
          {
            "text": "Evidence of major organ involvement such as lymphadenitis, hemophagocytosis, meningoencephalitis, persistent hepatitis, splenomegaly, interstitial pneumonitis, bone marrow hypoplasia, uveitis",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "splenomegaly, posterior cervical lymphadenopathy",
            "reasoning": "Patient has splenomegaly and lymphadenitis meeting major organ involvement criterion"
          },
          {
            "text": "Detection of elevated levels of EBV DNA, RNA or proteins in affected tissues OR elevated levels of EBV DNA in the peripheral blood",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No data on EBV DNA, RNA, or protein levels in tissues or peripheral blood provided"
          },
          {
            "text": "Any other condition that, in the opinion of the investigator, would make the patient unsuitable for enrollment or could interfere with the patient participating in the study",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": null,
            "reasoning": "No other conditions documented that would make patient unsuitable for enrollment"
          },
          {
            "text": "Age 3 years and above",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "19-year-old male",
            "reasoning": "Patient is 19 years old, which exceeds minimum age requirement of 3 years"
          },
          {
            "text": "Healthy relative of a CAEBV patient",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "fever, sore throat, fatigue, splenomegaly",
            "reasoning": "Patient is acutely ill with EBV; not healthy and not documented as CAEBV relative"
          },
          {
            "text": "Age 18 years and above",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "19-year-old male",
            "reasoning": "Patient is 19 years old, which meets minimum age requirement of 18 years"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Acute EBV with splenomegaly meets organ-involvement criterion; lacks chronic-progressive CAEBV features."
      },
      {
        "nct_id": "NCT05778006",
        "title": "Multi-Center Registry for ME/CFS",
        "phase": "NA",
        "criteria": [
          {
            "text": "ME/CFS diagnosis (ICD-10 G93.3) based on internationally established criteria",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "Monospot test is positive",
            "reasoning": "Positive monospot indicates acute infectious mononucleosis, not ME/CFS diagnosis"
          },
          {
            "text": "Informed consent by patients and/or guardian(s)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about informed consent in the vignette"
          },
          {
            "text": "No ME/CFS (ICD-10 G93.3)",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Monospot test is positive",
            "reasoning": "Patient has acute mononucleosis, not ME/CFS diagnosis"
          },
          {
            "text": "No informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information provided about informed consent status"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Lacks required ME/CFS diagnosis; has acute infectious mononucleosis, not chronic fatigue syndrome."
      },
      {
        "nct_id": "NCT06005246",
        "title": "Munich ME/CFS Cohort Study",
        "phase": "NA",
        "criteria": [
          {
            "text": "Written consent of the patient (or legal guardian for patients aged < 18 years)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about consent status in vignette"
          },
          {
            "text": "Age 0-25 (including)",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "A 19-year-old male",
            "reasoning": "Patient age 19 within inclusion range 0-25 years"
          },
          {
            "text": "Documented or probable acute infectious disease at the onset of ME/CFS symptoms",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "fever, sore throat, fatigue, monospot test is positive",
            "reasoning": "Acute infection documented but ME/CFS diagnosis not mentioned; unclear if infection at ME/CFS onset"
          },
          {
            "text": "Diagnosis of ME/CFS according to the IOM criteria, the CCC, the diagnostic worksheet published by P.C. Rowe et al. (2017), or the pediatric case definition published by L.A. Jason et al. (2006)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No ME/CFS diagnosis by any specified criteria documented"
          },
          {
            "text": "Drug/medication abuse",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No substance abuse history provided"
          },
          {
            "text": "Major surgery within the last six months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No surgical history mentioned"
          },
          {
            "text": "Presence of organ failure",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No organ failure evident; splenomegaly present but functioning"
          },
          {
            "text": "Hepatitis B/C",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No hepatitis serology or history documented"
          },
          {
            "text": "Multiple sclerosis",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "Acute infection presentation; no neurological signs of MS"
          },
          {
            "text": "Malignancy",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "Acute infectious presentation inconsistent with malignancy"
          },
          {
            "text": "Major depression or other severe psychiatric illness",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No psychiatric evaluation or mood disorder history documented"
          },
          {
            "text": "Severe endocrine disease (e.g., hypopituitarism, adrenal insufficiency)",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No endocrine dysfunction evident in acute infection presentation"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "No ME/CFS diagnosis; multiple exclusion criteria met: organ failure, MS, malignancy, endocrine disease."
      }
    ],
    "questions": [
      {
        "field": "Medical and Social History",
        "question": "Does patient have history of autoimmune disease, immunodeficiency, immunosuppressive therapy, substance abuse, or psychiatric illness?",
        "why": "Screen for exclusion criteria affecting 7 enrollment gates"
      },
      {
        "field": "EBV Serology and Viral Load",
        "question": "What are patient's EBV serology results (VCA-IgM/IgG, EBNA) and quantitative viral load?",
        "why": "Confirm primary infection and viral activity; impacts 4 trials"
      },
      {
        "field": "Informed Consent Status",
        "question": "Can patient independently provide informed written consent?",
        "why": "Verify consent capacity; mandatory for all trials"
      }
    ],
    "reeval": {
      "extended_record": "Patient denies any history of autoimmune disease, immunodeficiency, immunosuppressive therapy, or significant substance use. Psychiatric history is notable only for mild anxiety during high school, managed with reassurance, with no current symptoms or treatment. EBV serology from day 4 of illness shows VCA-IgM positive, VCA-IgG positive, and EBNA negative, consistent with acute primary EBV infection. Quantitative EBV DNA PCR measured 3.2 × 10^5 copies/mL on day 5. Patient demonstrates clear understanding of trial procedures, risks, and benefits, and expresses willingness to participate. Capacity assessment confirms patient can make independent healthcare decisions and has signed informed consent without hesitation.",
      "answers": [
        {
          "question": "Does patient have history of autoimmune disease, immunodeficiency, immunosuppressive therapy, substance abuse, or psychiatric illness?",
          "answer": "No significant history of autoimmune disease, immunodeficiency, or immunosuppressive therapy; no substance abuse; psychiatric history limited to mild anxiety during high school managed with reassurance, currently asymptomatic.",
          "evidence_quote": "Patient denies any history of autoimmune disease, immunodeficiency, immunosuppressive therapy, or significant substance use. Psychiatric history is notable only for mild anxiety during high school, managed with reassurance, with no current symptoms or treatment."
        },
        {
          "question": "What are patient's EBV serology results (VCA-IgM/IgG, EBNA) and quantitative viral load?",
          "answer": "VCA-IgM positive, VCA-IgG positive, EBNA negative; quantitative EBV DNA PCR 3.2 × 10^5 copies/mL on day 5 of illness.",
          "evidence_quote": "EBV serology from day 4 of illness shows VCA-IgM positive, VCA-IgG positive, and EBNA negative, consistent with acute primary EBV infection. Quantitative EBV DNA PCR measured 3.2 × 10^5 copies/mL on day 5."
        },
        {
          "question": "Can patient independently provide informed written consent?",
          "answer": "Yes. Patient demonstrates clear understanding of trial procedures, risks, and benefits, and has capacity to make independent healthcare decisions.",
          "evidence_quote": "Patient demonstrates clear understanding of trial procedures, risks, and benefits, and expresses willingness to participate. Capacity assessment confirms patient can make independent healthcare decisions and has signed informed consent without hesitation."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT05127980",
          "criterion": "Informed consent as documented by signature",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "Serology compatible with primary EBV infection: anti-EBNA IgG negative, anti-VCA IgG negative, anti-VCA IgM positive",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "Serology compatible with primary EBV infection: anti-EBNA IgG negative, anti-VCA IgG positive, anti-VCA IgM positive",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "Primary or secondary immunodeficiency",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "Treatment with immunosuppressive medication including ≥10mg prednisone equivalent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "History of autoimmune disease such as systemic lupus erythematosus or vasculitis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05778006",
          "criterion": "Informed consent by patients and/or guardian(s)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05778006",
          "criterion": "No informed consent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Written consent of the patient (or legal guardian for patients aged < 18 years)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Drug/medication abuse",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Major depression or other severe psychiatric illness",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT00032513",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Primary EBV infection with splenomegaly (major organ involvement); meets inclusion criteria. Uncertain if acute presentation meets 'severe progressive' or 'chronic active' criteria."
        },
        {
          "nct_id": "NCT05127980",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Primary EBV confirmed clinically and serologically. Most inclusions met. Multiple exclusion criteria present (immunodeficiency, immunosuppressive medication, autoimmune disease history)."
        },
        {
          "nct_id": "NCT05778006",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Patient presents with acute primary EBV, not myalgic encephalomyelitis/chronic fatigue syndrome (ME/CFS). Does not meet primary inclusion criterion."
        },
        {
          "nct_id": "NCT06005246",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Acute primary EBV, not ME/CFS diagnosis. Lacks ME/CFS inclusion criterion; multiple exclusion criteria documented (organ failure, severe psychiatric illness)."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S010",
    "patient_text": "A 73-year-old man with sudden onset of a painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters.",
    "extraction": [
      {
        "name": "Age",
        "value": "73 years old",
        "evidence_quote": "73-year-old"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "man"
      },
      {
        "name": "Onset of vision loss",
        "value": "Sudden",
        "evidence_quote": "sudden onset"
      },
      {
        "name": "Vision loss characteristics",
        "value": "Painless, curtain-like loss of vision",
        "evidence_quote": "painless, curtain-like loss of vision in the right eye"
      },
      {
        "name": "Laterality",
        "value": "Right eye",
        "evidence_quote": "right eye"
      },
      {
        "name": "Prodromal symptom - photopsia",
        "value": "Flashes of light",
        "evidence_quote": "flashes of light"
      },
      {
        "name": "Prodromal symptom - floaters",
        "value": "Floaters",
        "evidence_quote": "floaters"
      },
      {
        "name": "Temporal relationship",
        "value": "Preceded by flashes and floaters",
        "evidence_quote": "preceded by flashes of light and floaters"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06587945",
        "title": "Nicotinamide Riboside Oral Supplementation in Macula Off Retinal Detachment",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Age ≥ 18 years old",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "73-year-old man",
            "reasoning": "Patient is 73 years old"
          },
          {
            "text": "Able to give informed consent and comply with all study visits and procedures",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about consent capacity provided"
          },
          {
            "text": "Present within 10 days of macula-off retinal detachment (based on patient-reported history of loss of central vision)",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "evidence": "sudden onset of a painless, curtain-like loss of vision in the right eye",
            "reasoning": "Timing and macula-off status unclear from clinical presentation"
          },
          {
            "text": "Present to the hospital with a visual acuity of hand motion or better in the study eye",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No visual acuity measurements documented in vignette"
          },
          {
            "text": "Have had previous cataract surgery in the study eye",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior ocular surgery history documented"
          },
          {
            "text": "Have clinical indication for standard retinal reattachment surgery by means of a pars plana vitrectomy and gas tamponade",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "sudden onset of a painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters",
            "reasoning": "Classic retinal detachment presentation with standard surgical indication"
          },
          {
            "text": "Any known significant ocular disease in the study eye (e.g., cornea opacity) which, in the opinion of the investigator, would preclude a visual acuity of at least 6/7.5 (20/25) following successful vitrectomy or limit adequate visibility of the retina",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No documented significant ocular disease beyond retinal detachment"
          },
          {
            "text": "History of previous ocular surgery in the study eye other than uncomplicated cataract surgery with posterior chamber intraocular lens and intact posterior capsule or a refractive surgery (surgery must have occurred at least 3 months prior to the baseline visit)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No prior ocular surgery history documented"
          },
          {
            "text": "Known retinopathy, known hepatic disease (or history of significant chronic liver disease), or known renal disease",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No documented systemic disease history in vignette"
          },
          {
            "text": "History of uncontrolled hypertension",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No blood pressure or hypertension information provided"
          },
          {
            "text": "History of stroke, transient ischemic attack, or major cardiac surgery within 3 months prior to study, or current treatment for systemic infection",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": null,
            "reasoning": "No documented cardiovascular events or systemic infection"
          },
          {
            "text": "Females who are pregnant or lactating and women of childbearing potential",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "73-year-old man",
            "reasoning": "Patient is male; criterion applies only to females"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 1,
        "rationale": "Macula-off RRD-specific trial; age and surgical indication criteria met. Multiple systemic exclusions flagged (retinopathy, hepatic/renal disease, cardiac) not mentioned in vignette."
      },
      {
        "nct_id": "NCT07346560",
        "title": "1ry Versus 2ry ILM Peeling in RD",
        "phase": "NA",
        "criteria": [
          {
            "text": "Uncomplicated rhegmatogenous retinal detachment",
            "type": "inclusion",
            "verdict": "MET",
            "evidence": "Sudden onset of painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters",
            "reasoning": "Classic presentation of uncomplicated rhegmatogenous retinal detachment"
          },
          {
            "text": "PVR",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Sudden onset painless curtain-like vision loss with floaters and photopsia; no mention of advanced proliferation",
            "reasoning": "Acute presentation without clinical signs of PVR"
          },
          {
            "text": "Recurrent RD",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Sudden onset",
            "reasoning": "No prior history of detachment; initial presentation"
          },
          {
            "text": "Tractional RD",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Sudden onset of painless curtain-like loss preceded by floaters and photopsia",
            "reasoning": "Clinical presentation consistent with rhegmatogenous, not tractional mechanism"
          },
          {
            "text": "Macular hole RD",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No explicit description of macular involvement or macular hole present"
          },
          {
            "text": "Scleral buckling is indicated",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Detachment location and characteristics not specified; cannot determine surgical approach"
          },
          {
            "text": "Macular scarring",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "Sudden onset",
            "reasoning": "Acute presentation with no evidence of chronic scarring"
          },
          {
            "text": "Previous PPV",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "No surgical history mentioned in vignette",
            "reasoning": "No prior vitreoretinal surgery documented"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Uncomplicated RRD trial, fewest UNKNOWN criteria (2). Exclusions met (PVR, recurrent, tractional RD, scarring, prior PPV) inconsistent with acute presentation."
      },
      {
        "nct_id": "NCT07081945",
        "title": "hAM for Inferior RRD",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 18-70 years old",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "evidence": "73-year-old man",
            "reasoning": "Patient age exceeds maximum inclusion limit of 70 years"
          },
          {
            "text": "RRD with inferior retinal breaks between 4- and 8-o'clock within the detached area regardless of PVR grade",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Retinal break location, size, and relationship to detached area not specified"
          },
          {
            "text": "RRD requiring retinotomy inferiorly between 4- and 8-o'clock due to severe inferior PVR or inferior retinal shortening",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Surgical indication and PVR severity details not provided in vignette"
          },
          {
            "text": "Free and informed consent to take part in the study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Patient consent status not addressed in clinical presentation"
          },
          {
            "text": "RRD with only anterior retina breaks or dialysis meeting indications for scleral buckling surgery",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "Curtain-like loss of vision",
            "reasoning": "Presentation consistent with inferior RD involvement, not anterior-only breaks"
          },
          {
            "text": "RRD with retinal breaks located between 4- and 8-o'clock positions not involved in the detached area",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Specific retinal break location and relationship to detached area not documented"
          },
          {
            "text": "Pre-existing serious eye diseases such as corneal ulcers, glaucoma, uveitis",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "evidence": "Sudden onset of painless vision loss; no prior ocular disease mentioned",
            "reasoning": "No evidence of pre-existing corneal ulcers, glaucoma, or uveitis"
          },
          {
            "text": "History of epilepsy or serious psychiatric diseases",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Psychiatric and neurologic history not provided in vignette"
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Patient 73 years old exceeds trial age limit of 70. Definitive age-based ineligibility; other RRD criteria remain largely unknown."
      },
      {
        "nct_id": "NCT07228091",
        "title": "Surgical Procedure Efficiency Evaluation stuDy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Able to understand and sign an informed consent form (ICF) that has been approved by an ethics committee",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about cognition or consent capacity."
          },
          {
            "text": "Planned combined phacovitrectomy procedure at one of the selected surgical sites",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about planned surgical procedure or site selection."
          },
          {
            "text": "Planned combined phacovitrectomy procedure with 25-gauge (G) vitrectomy tools",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about planned surgery or vitrectomy gauge specifications."
          },
          {
            "text": "Unplanned/emergency phacovitrectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Sudden presentation suggests possible emergency, but not explicitly stated."
          },
          {
            "text": "Pregnant",
            "type": "exclusion",
            "verdict": "MET",
            "evidence": "73-year-old man",
            "reasoning": "Patient is male; pregnancy exclusion clearly not applicable."
          },
          {
            "text": "Past history of phacovitrectomy, cataract, vitrectomy in the planned operative eye",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "No information about past ocular surgery history."
          },
          {
            "text": "Other protocol-defined exclusion criteria may apply",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "evidence": null,
            "reasoning": "Cannot assess undefined protocol exclusion criteria from vignette alone."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Phacovitrectomy efficiency study with 7 UNKNOWN criteria. Pregnancy exclusion flagged; unclear if combined cataract surgery is clinically needed for this patient."
      }
    ],
    "questions": [
      {
        "field": "Retinal break location and characteristics",
        "question": "What is the exact location of the retinal break (e.g., 4 o'clock, 8 o'clock position) and its relationship to the area of retinal detachment?",
        "why": "Specific break location determines eligibility for multiple trial protocols"
      },
      {
        "field": "Macular involvement and symptom timeline",
        "question": "Exactly how many days have passed since symptom onset, and is the macula currently attached or involved in the detachment?",
        "why": "Determines 10-day eligibility window and macula-on vs macula-off status"
      },
      {
        "field": "Previous ocular surgery in affected eye",
        "question": "Has the patient had any prior eye surgery (cataract extraction, vitrectomy, or laser procedures) in the right eye?",
        "why": "Prior procedures affect eligibility criteria across multiple trials"
      }
    ],
    "reeval": {
      "extended_record": "On post-symptom day 4, ophthalmologic examination confirmed a superior temporal rhegmatogenous retinal detachment in the right eye with the macula remaining attached. The retinal break was identified at approximately the 11 o'clock position, measuring 2.5 mm in size. The detachment extended inferiorly and nasally from the site of the break, encompassing approximately 40% of the retina. Spectral-domain OCT confirmed that the macula remained attached, with foveal thickness of 238 micrometers (normal 200–260 μm). Anterior segment examination revealed a clear lens without evidence of prior cataract surgery. The patient reported no history of prior vitrectomy or laser procedures in the right eye. Intraocular pressures were 14 mmHg (OD) and 15 mmHg (OS). The left eye examination was unremarkable.",
      "answers": [
        {
          "question": "What is the exact location of the retinal break (e.g., 4 o'clock, 8 o'clock position) and its relationship to the area of retinal detachment?",
          "answer": "The retinal break is located at the 11 o'clock position (2.5 mm), with the detachment extending inferiorly and nasally from the break, encompassing approximately 40% of the retina.",
          "evidence_quote": "The retinal break was identified at approximately the 11 o'clock position, measuring 2.5 mm in size. The detachment extended inferiorly and nasally from the site of the break, encompassing approximately 40% of the retina."
        },
        {
          "question": "Exactly how many days have passed since symptom onset, and is the macula currently attached or involved in the detachment?",
          "answer": "4 days have passed since symptom onset, and the macula is currently attached (not involved in the detachment).",
          "evidence_quote": "On post-symptom day 4, ophthalmologic examination confirmed a superior temporal rhegmatogenous retinal detachment in the right eye with the macula remaining attached."
        },
        {
          "question": "Has the patient had any prior eye surgery (cataract extraction, vitrectomy, or laser procedures) in the right eye?",
          "answer": "No prior eye surgery. The patient has a clear lens (no cataract surgery) and no history of vitrectomy or laser procedures.",
          "evidence_quote": "Anterior segment examination revealed a clear lens without evidence of prior cataract surgery. The patient reported no history of prior vitrectomy or laser procedures in the right eye."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06587945",
          "criterion": "Present within 10 days of macula-off retinal detachment (based on patient-reported history of loss of central vision)",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "Have had previous cataract surgery in the study eye",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "History of previous ocular surgery in the study eye other than uncomplicated cataract surgery with posterior chamber intraocular lens and intact posterior capsule or a refractive surgery (surgery must have occurred at least 3 months prior to the baseline visit)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07346560",
          "criterion": "Macular hole RD",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "RRD with inferior retinal breaks between 4- and 8-o'clock within the detached area regardless of PVR grade",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "RRD requiring retinotomy inferiorly between 4- and 8-o'clock due to severe inferior PVR or inferior retinal shortening",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "RRD with retinal breaks located between 4- and 8-o'clock positions not involved in the detached area",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07228091",
          "criterion": "Past history of phacovitrectomy, cataract, vitrectomy in the planned operative eye",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06587945",
          "rank": 1,
          "eligibility": "INELIGIBLE",
          "rationale": "RD-specific trial, vitrectomy indication met, but macula-off timing/status uncertain; retinopathy exclusion met."
        },
        {
          "nct_id": "NCT07346560",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Uncomplicated RRD inclusion met but five complication exclusions met: PVR, recurrence, traction, scarring, prior vitrectomy."
        },
        {
          "nct_id": "NCT07228091",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Unknown if combined phacovitrectomy planned; pregnancy exclusion MET (likely data error for male patient)."
        },
        {
          "nct_id": "NCT07081945",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Age 73 exceeds 70-year limit; lacks required inferior retinal break pattern; retinotomy criteria not met."
        }
      ]
    },
    "generated_at": "2026-07-08"
  }
];
