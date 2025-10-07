# Conexões

| workflow | from | to | path |
| --- | --- | --- | --- |
| 1. Atendente.V2.0 | Mensagem chegando? | Tipo de mensagem | main |
| 1. Atendente.V2.0 | Mensagem recebida | Info | main |
| 1. Atendente.V2.0 | Mensagem encavalada? | Limpar fila de mensagens | main |
| 1. Atendente.V2.0 | Buscar mensagens | Mensagem encavalada? | main |
| 1. Atendente.V2.0 | Concatenar mensagens | Atendente | main |
| 1. Atendente.V2.0 | Limpar fila de mensagens | controle atendimentos | main |
| 1. Atendente.V2.0 | Esperar | Buscar mensagens | main |
| 1. Atendente.V2.0 | Tipo de mensagem | Enfileirar mensagem. | main |
| 1. Atendente.V2.0 | Tipo de mensagem | HTTP Request1 | main |
| 1. Atendente.V2.0 | Transcrever áudio | controle atendimentos1 | main |
| 1. Atendente.V2.0 | Resetar status | Responder mensagem áudio | main |
| 1. Atendente.V2.0 | Converter áudio para base64 | Resetar status | main |
| 1. Atendente.V2.0 | Gerar áudio | Converter áudio para base64 | main |
| 1. Atendente.V2.0 | Formatar SSML | Gerar áudio | main |
| 1. Atendente.V2.0 | Tipo de mensagem1 | Code | main |
| 1. Atendente.V2.0 | Tipo de mensagem1 | Formatar SSML | main |
| 1. Atendente.V2.0 | Memory | Atendente | ai_memory |
| 1. Atendente.V2.0 | Converter base64 para áudio. | Transcrever áudio | main |
| 1. Atendente.V2.0 | Enfileirar mensagem. | Esperar | main |
| 1. Atendente.V2.0 | Google Gemini Chat Model. | Formatar SSML | ai_languageModel |
| 1. Atendente.V2.0 | Info | Mensagem chegando? | main |
| 1. Atendente.V2.0 | Atendente | atualiza atendimento | main |
| 1. Atendente.V2.0 | enviar_pedido | Atendente | ai_tool |
| 1. Atendente.V2.0 | maps | Atendente | ai_tool |
| 1. Atendente.V2.0 | cardapio | Atendente | ai_tool |
| 1. Atendente.V2.0 | cancelar_pedido | Atendente | ai_tool |
| 1. Atendente.V2.0 | Code | Loop Over Items | main |
| 1. Atendente.V2.0 | Loop Over Items | HTTP Request | main |
| 1. Atendente.V2.0 | HTTP Request | Loop Over Items | main |
| 1. Atendente.V2.0 | Concatenar mensagens1 | Atendente | main |
| 1. Atendente.V2.0 | HTTP Request1 | Converter base64 para áudio. | main |
| 1. Atendente.V2.0 | HTTP Request1 | HTTP Request2 | main |
| 1. Atendente.V2.0 | HTTP Request2 | Converter base64 para áudio. | main |
| 1. Atendente.V2.0 | historico | Atendente | ai_tool |
| 1. Atendente.V2.0 | Marcar como lida texto | Concatenar mensagens | main |
| 1. Atendente.V2.0 | controle atendimentos | Marcar como lida texto | main |
| 1. Atendente.V2.0 | atualiza atendimento | Tipo de mensagem1 | main |
| 1. Atendente.V2.0 | Marcar como lida audio | Concatenar mensagens1 | main |
| 1. Atendente.V2.0 | Google Gemini Chat Model | Atendente | ai_languageModel |
| 1. Atendente.V2.0 | controle atendimentos1 | Marcar como lida audio | main |
