#!/usr/bin/env python3
import os
import json
import zipfile
import xml.etree.ElementTree as ET

def extract_docx_text(docx_path):
    if not os.path.exists(docx_path):
        return ""
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            texts = []
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            for elem in root.findall('.//w:t', namespaces):
                texts.append(elem.text)
            return ''.join(texts)
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return ""

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo_dir = os.path.join(base_dir, "documentary-repository", "Judgements for Review Paperes")
    out_dir = os.path.join(base_dir, "data")
    
    # 1. Ingest Islamabad High Court Margalla Hills National Park docx extracts
    ihc_doc_path = os.path.join(repo_dir, "ISD National Park Judgment", "Extracts of IHC National Park Judgemnet.docx")
    ihc_review_path = os.path.join(repo_dir, "ISD National Park Judgment", "Judgement Review - ISD National Park - IHC -  -KSC- 13.7.2022.docx")
    
    ihc_text = extract_docx_text(ihc_doc_path)
    ihc_review_text = extract_docx_text(ihc_review_path)
    
    # Clean up the text slightly for JSON compatibility
    ihc_text_clean = ihc_text.strip().replace("\r", "\n")
    ihc_review_clean = ihc_review_text.strip().replace("\r", "\n")
    
    # 2. Compile Judgments List
    judgments = [
        {
            "id": "ihc_national_park_2022",
            "name": "Malik Bashir Ahmed v. The Federal Government of Pakistan (Margalla Hills National Park Case)",
            "citation": "Writ Petition No. 308 of 2016 (IHC)",
            "court": "Islamabad High Court",
            "date": "2022-01-11",
            "judge": "Chief Justice Athar Minallah",
            "articles": ["article-009", "article-199"],
            "amendments": [],
            "impact": "Environmental preservation and climate stability declared intrinsic to the Right to Life (Article 9). Encroachments by state/military agencies declared illegal under Public Trust Doctrine.",
            "factual_background": "Professor Zahid Baig Mirza and other environmental activists challenged commercialized construction inside the Margalla Hills National Park (including the Monal Restaurant and navy sailing clubs built on park land). The court reviewed the legal mandate of the Capital Development Authority (CDA) and the Ministry of Defence over military-held areas in the park.",
            "holdings": [
                "The Right to Life guaranteed under Article 9 is dependent on a clean, functioning ecological system; state failure to protect biodiversity is a direct violation of Article 9.",
                "Margalla Hills National Park is protected land under the Islamabad Wildlife Ordinance 1979. Any lease, commercial activity (such as Monal Restaurant), or military construction (navy sailing club) inside the park is illegal and void.",
                "The Public Trust Doctrine dictates that the State is a fiduciary trustee of natural resources for the benefit of citizens and cannot alienate or commercialize them for elite interests.",
                "Martial Law Regulations (like MLR 82) do not grant military authorities property rights over national park land."
            ],
            "raw_extracts": ihc_text_clean[:6000] + "\n\n[Truncated for performance...]",
            "commentary": ihc_review_clean[:6000] + "\n\n[Truncated for performance...]"
        },
        {
            "id": "lhc_climate_2015",
            "name": "Asghar Leghari v. Federation of Pakistan (Green Bench Climate Case)",
            "citation": "Writ Petition No. 25501 of 2015 (LHC)",
            "court": "Lahore High Court",
            "date": "2015-09-04",
            "judge": "Justice Syed Mansoor Ali Shah",
            "articles": ["article-009", "article-014"],
            "amendments": [],
            "impact": "Established the Climate Change Commission (CCC). Enforced Climate Change Policy as a fundamental right obligation under Article 9 (Life) and Article 14 (Dignity).",
            "factual_background": "A farmer, Asghar Leghari, filed a writ petition in the Lahore High Court stating that the Federal and Provincial governments had failed to implement the National Climate Change Policy 2012 and the Framework for Implementation of Climate Change Policy (2014-2030), directly threatening water, food, and energy security.",
            "holdings": [
                "Climate change is no longer a future threat but an active crisis. Delay in implementing climate adaptation policy violates the right to life (Article 9) and human dignity (Article 14).",
                "Environmental justice demands a shift from anthropocentric (human-centered) to ecocentric (nature-centered) jurisprudence to protect ecosystems.",
                "Constituted a Climate Change Commission (CCC) composed of government secretaries, experts, and NGOs to monitor and enforce climate change policy actions.",
                "Established specialized 'Green Benches' in the High Courts to fast-track environmental litigation and resolve ecological issues."
            ],
            "raw_extracts": "The delay in implementing the National Climate Change Policy 2012 violates the fundamental rights of citizens. The right to life under Article 9, read with human dignity under Article 14, encompasses the right to a clean and healthy environment. Environmental degradation, water scarcity, and food insecurity caused by climate change pose a direct threat to the survival of the human species in Pakistan. The State must act as a proactive trustee to enforce environmental and climate justice policies.",
            "commentary": "Asghar Leghari is recognized globally as a pioneering judgment in climate change litigation. By creating the Climate Change Commission, the Lahore High Court bypassed executive lethargy and directly supervised the implementation of climate adaptation measures. This case firmly anchored climate justice in the constitutional framework of Pakistan."
        }
    ]
    
    # Write judgments.json
    out_json_path = os.path.join(out_dir, "judgments.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(judgments, f, ensure_ascii=False, separators=(",", ":"))
        
    # Write judgments.js
    out_js_path = os.path.join(out_dir, "judgments.js")
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated judgments database. Do not edit manually. */\n")
        f.write("window.JUDGMENTS_DATA = ")
        json.dump(judgments, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
        
    print(f"Compiled judgments database: {len(judgments)} landmark judgments indexed.")
    print(f"Wrote {out_json_path} and {out_js_path}")

if __name__ == "__main__":
    main()
