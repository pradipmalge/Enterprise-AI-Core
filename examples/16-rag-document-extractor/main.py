import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent
from enterprise_ai_core.rag import (
    ingest_document_to_rag,
    extract_document_details,
    search_knowledge_base,
)

SAMPLE_ENTERPRISE_SLA = """
ENTERPRISE SERVICE LEVEL AGREEMENT (SLA) & FINANCIAL TERMS 2026

1. COMMENCEMENT & PARTIES
This Service Level Agreement is effective from March 1, 2026 through February 28, 2028.
Parties: Apex Cloud Infrastructure Inc ("Provider") and Global Enterprise Corp ("Client").

2. SERVICE AVAILABILITY & SLA METRICS
- System Uptime Commitment: Provider guarantees 99.99% monthly uptime for Core Cloud APIs.
- Penalty Credits: If uptime falls below 99.90%, Client receives 15% billing credit.
- Response Time SLA: Severity 1 incidents shall be acknowledged within 15 minutes.

3. FINANCIAL CONSIDERATIONS & PRICING
- Annual Base Contract Value: $1,250,000 USD billed quarterly in advance ($312,500 USD per quarter).
- Overage Rate: Excess compute hours billed at $0.045 per vCPU hour.
- Payment Terms: Net 30 days.

4. COMPLIANCE & SECURITY GOVERNANCE
- Data Sovereignty: All Client data hosted within EU-Central-1 and US-East-1 regions.
- Certifications: Provider maintains SOC2 Type II, ISO 27001, and HIPAA compliance.
"""

async def main():
    print("=== Phase 24: Enterprise RAG & Document Details Extractor ===")
    
    # 1. Ingest document text into vector knowledge base
    print("\n[Step 1] Ingesting document chunks into Vector Index...")
    ingest_res = ingest_document_to_rag(SAMPLE_ENTERPRISE_SLA, source_name="Apex_Cloud_SLA_2026.pdf")
    print(ingest_res)

    # 2. Directly extract structured entity details
    print("\n[Step 2] Executing Document Extractor Tool...")
    details = extract_document_details(SAMPLE_ENTERPRISE_SLA)
    print(details)

    # 3. Build Enterprise Agent with RAG Tools
    print("\n[Step 3] Building Enterprise Agent with RAG tools registered...")
    agent = (
        EnterpriseAgent.builder()
        .use_gemini()
        .use_memory_cache()
        .register_tool(extract_document_details)
        .register_tool(search_knowledge_base)
        .register_tool(ingest_document_to_rag)
        .build()
    )

    # 4. Prompt agent for RAG question answering
    prompt = "What is the uptime SLA percentage, penalty credit rate, and quarterly billing amount in the SLA contract?"
    print(f"\n[Step 4] Prompting Agent: '{prompt}'")
    response = await agent.chat(prompt)
    print("\nAgent Output:")
    print(json.dumps(response.value, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
