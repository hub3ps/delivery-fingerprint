# Nós

| workflow | id | name | type | disabled |
| --- | --- | --- | --- | --- |
| 1. Atendente.V2.0 | 8a72a161-0618-4503-b20f-d0469beed592 | Mensagem chegando? | n8n-nodes-base.filter | False |
| 1. Atendente.V2.0 | 685cbd5e-4b57-4c14-a645-571552eb1b09 | Mensagem recebida | n8n-nodes-base.webhook | False |
| 1. Atendente.V2.0 | 685b4efd-6fc5-42fb-bfe8-2524da1d3b82 | Mensagem encavalada? | n8n-nodes-base.code | False |
| 1. Atendente.V2.0 | 1e30c84f-596b-4610-8995-78d927b4b716 | Buscar mensagens | n8n-nodes-base.postgres | False |
| 1. Atendente.V2.0 | 1f14fd1e-6afd-440f-9200-1cb2cb9ab754 | Concatenar mensagens | n8n-nodes-base.set | False |
| 1. Atendente.V2.0 | 9c2039ea-b4e6-4f2e-9a7b-d7bc2de2fff2 | Limpar fila de mensagens | n8n-nodes-base.postgres | False |
| 1. Atendente.V2.0 | 20ffecd1-911a-4348-8bfb-1da651d73a7a | Sticky Note2 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | 067374e9-e81a-4416-b8ea-432de5fe9ce0 | Esperar | n8n-nodes-base.wait | False |
| 1. Atendente.V2.0 | 93183e23-c2bf-4761-b814-47dde30399ac | Sticky Note3 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | 3578eedb-c388-44f8-b996-b7c40d0a7781 | Sticky Note4 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | ec8af50d-7a4d-480f-9f4c-ec025c76efbb | Sticky Note5 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | 3688aeaa-e61c-47a3-be73-bdbc36174e59 | Tipo de mensagem | n8n-nodes-base.switch | False |
| 1. Atendente.V2.0 | b8abd4eb-f56f-4570-aa46-665c6101c850 | Transcrever áudio | @n8n/n8n-nodes-langchain.openAi | False |
| 1. Atendente.V2.0 | 402f6d26-0a9f-48e5-a3c3-690917a6434d | Sticky Note6 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | 4052a095-7196-4d9d-9481-cd574821682f | Resetar status | n8n-nodes-evolution-api.evolutionApi | True |
| 1. Atendente.V2.0 | 956ae855-b2e9-47fd-8faa-7ec425639228 | Converter áudio para base64 | n8n-nodes-base.extractFromFile | True |
| 1. Atendente.V2.0 | 7642be87-198b-434d-9218-6adc2ac27a73 | Sticky Note12 | n8n-nodes-base.stickyNote | False |
| 1. Atendente.V2.0 | fc3a9b77-d153-448b-b216-e5c7574ecccc | Gerar áudio | n8n-nodes-base.httpRequest | True |
| 1. Atendente.V2.0 | 13d7f835-9b44-4857-80a6-f09b219738ac | Formatar SSML | @n8n/n8n-nodes-langchain.chainLlm | True |
| 1. Atendente.V2.0 | bb584de7-c64b-4f30-85c1-0d65ead67330 | Tipo de mensagem1 | n8n-nodes-base.switch | False |
| 1. Atendente.V2.0 | 25436fec-8353-4071-868f-9e8ff32cec54 | Memory | @n8n/n8n-nodes-langchain.memoryPostgresChat | False |
| 1. Atendente.V2.0 | 320a4087-1431-45f6-a832-1d15f501000f | Escalar humano | n8n-nodes-base.telegramTool | True |
| 1. Atendente.V2.0 | fb43d770-946a-434d-957c-41490532cdec | Responder mensagem áudio | n8n-nodes-evolution-api.evolutionApi | True |
| 1. Atendente.V2.0 | 02a2ff2b-79d2-455a-910c-c407bff03dad | Converter base64 para áudio. | n8n-nodes-base.convertToFile | False |
| 1. Atendente.V2.0 | ba9f3c35-3220-45a2-97f7-fc9b4dcebf84 | Enfileirar mensagem. | n8n-nodes-base.postgres | False |
| 1. Atendente.V2.0 | fe96a8b0-bf88-45ec-bc07-d59ca358a5fb | Google Gemini Chat Model. | @n8n/n8n-nodes-langchain.lmChatGoogleGemini | True |
| 1. Atendente.V2.0 | 3b37babf-24fc-4300-9933-38e988eb1a78 | Info | n8n-nodes-base.set | False |
| 1. Atendente.V2.0 | 52f1bee1-6480-4b39-aa5e-e90b8a39ca4b | Atendente | @n8n/n8n-nodes-langchain.agent | False |
| 1. Atendente.V2.0 | 6733466e-009b-45f6-b360-768e7d7dd7c9 | enviar_pedido | n8n-nodes-base.httpRequestTool | False |
| 1. Atendente.V2.0 | 03ad518e-5e22-48a0-a49b-bd70e754074d | maps | n8n-nodes-base.httpRequestTool | False |
| 1. Atendente.V2.0 | 7d265e35-0809-447e-85bf-9ab556005c8f | cardapio | n8n-nodes-base.postgresTool | False |
| 1. Atendente.V2.0 | 712191bc-00fa-434d-b8f4-ee167bff6c97 | cancelar_pedido | n8n-nodes-base.httpRequestTool | False |
| 1. Atendente.V2.0 | 416470f9-e557-4c8b-96c6-38a0e194cb85 | Code | n8n-nodes-base.code | False |
| 1. Atendente.V2.0 | cc55fc36-84c3-4881-94ec-6a5b7ac9e77d | Loop Over Items | n8n-nodes-base.splitInBatches | False |
| 1. Atendente.V2.0 | baaeb89d-9844-4c88-ac74-d8bccfb7f704 | HTTP Request | n8n-nodes-base.httpRequest | False |
| 1. Atendente.V2.0 | 386819d4-cf55-4771-afc2-c9e4d54f5a01 | Concatenar mensagens1 | n8n-nodes-base.set | False |
| 1. Atendente.V2.0 | 41672fc5-409d-46ef-9509-4ff4161d08a7 | HTTP Request1 | n8n-nodes-base.httpRequest | False |
| 1. Atendente.V2.0 | e925faa0-2924-4b88-a05d-83a77a4bfb44 | HTTP Request2 | n8n-nodes-base.httpRequest | False |
| 1. Atendente.V2.0 | 41d1aa3f-a692-46df-829a-166abbac3024 | historico | n8n-nodes-base.postgresTool | False |
| 1. Atendente.V2.0 | 7b8cba49-28cc-4597-becc-2bd8d9bca0dc | Marcar como lida texto | n8n-nodes-evolution-api.evolutionApi | False |
| 1. Atendente.V2.0 | ee36b3b9-f568-4dd0-9413-49f64889aa5e | controle atendimentos | n8n-nodes-base.postgres | False |
| 1. Atendente.V2.0 | 827649a3-892a-4735-8e4a-49fb83bbffe3 | atualiza atendimento | n8n-nodes-base.postgres | False |
| 1. Atendente.V2.0 | 584cfcf1-0a94-4dc3-bec2-e716fed066a9 | Marcar como lida audio | n8n-nodes-evolution-api.evolutionApi | False |
| 1. Atendente.V2.0 | e0309c9d-c2f0-48bb-9b00-d203d87e3919 | Google Gemini Chat Model | @n8n/n8n-nodes-langchain.lmChatGoogleGemini | False |
| 1. Atendente.V2.0 | fb2134a0-4d39-4e0a-8a97-05b4b6c9e081 | controle atendimentos1 | n8n-nodes-base.postgres | False |
