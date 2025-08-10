@echo off
echo  RETRYING FAILED REPOSITORY CLONES...
echo  Moving to external-agents directory...
cd external-agents

echo  Retrying Control Frameworks...
git clone https://github.com/OpenBMB/ChatDev.git control-chatdev-retry
git clone https://github.com/crewAIInc/crewAI.git control-crewai-retry

echo  Retrying Communication Agents...
git clone https://github.com/EvolutionAPI/evolution-api.git messaging-evolution-retry
git clone https://github.com/devlikeapro/waha.git messaging-waha-retry  
git clone https://github.com/WhatsApp/WhatsApp-Nodejs-SDK.git messaging-whatsapp-retry
git clone https://github.com/receevi/receevi.git messaging-receevi-retry

echo  Retrying Social Media Agent...
git clone https://github.com/nodejs-social-media-automation social-media-retry

echo  Retry attempt complete!
pause
