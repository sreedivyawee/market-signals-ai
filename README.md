# Market Signals AI

## Overview

Market Signals AI is a multi-agent financial intelligence system designed
to provide explainable and evidence-grounded investment insights for
retail investors.

The system combines specialized market-analysis agents, Retrieval-Augmented
Generation (RAG), and a synthesis layer to produce a unified investment
signal with confidence, reasoning, conflict detection, and supporting
sources.

---

## System Architecture

```text
                         Market Data
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
      Volatility Agent  Volume Agent    News Agent
             |               |               |
             +---------------+---------------+
                             |
                             v
                      Synthesis Agent
                             |
                   +---------+---------+
                   |                   |
                   v                   v
                  RAG             Agent Signals
                   |
                   v
             Financial Documents
                   |
                   v
           Relevant Evidence
                   |
                   v
          Source + Page Attribution
                   |
                   v
              Final Signal


https://hackverse-market-ai.ai.studio
