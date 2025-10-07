# Expressões

| workflow | node | param_path | expression | refs |
| --- | --- | --- | --- | --- |
| 1. Atendente.V2.0 | Mensagem chegando? | $.parameters.conditions.conditions[0].leftValue | $('Info').item.json.fromMe |  |
| 1. Atendente.V2.0 | Mensagem chegando? | $.parameters.conditions.conditions[1].leftValue | $('Info').item.json.mensagem_de_grupo |  |
| 1. Atendente.V2.0 | Mensagem chegando? | $.parameters.conditions.conditions[2].leftValue | ['text','audio'].includes($('Info').item.json.message_type) |  |
| 1. Atendente.V2.0 | Mensagem chegando? | $.parameters.conditions.conditions[3].leftValue | ( $('Info').item.json.telefone \|\| '' ).length >= 10 |  |
| 1. Atendente.V2.0 | Buscar mensagens | $.parameters.where.values[0].value | $json.telefone | json:$json |
| 1. Atendente.V2.0 | Buscar mensagens | $.parameters.where.values[1].value | $json.status | json:$json |
| 1. Atendente.V2.0 | Concatenar mensagens | $.parameters.assignments.assignments[0].value | $('Mensagem encavalada?').all().map(info => info.json.mensagem).join('\\n') |  |
| 1. Atendente.V2.0 | Concatenar mensagens | $.parameters.assignments.assignments[1].value | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Limpar fila de mensagens | $.parameters.where.values[0].value | $json.telefone | json:$json |
| 1. Atendente.V2.0 | Tipo de mensagem | $.parameters.rules.values[0].conditions.conditions[0].leftValue | $('Info').item.json.message_type === 'text' |  |
| 1. Atendente.V2.0 | Tipo de mensagem | $.parameters.rules.values[1].conditions.conditions[0].leftValue | $('Info').item.json.message_type === 'audio' |  |
| 1. Atendente.V2.0 | Tipo de mensagem | $.parameters.rules.values[2].conditions.conditions[0].leftValue | ['text','audio'].includes($('Info').item.json.message_type) |  |
| 1. Atendente.V2.0 | Resetar status | $.parameters.instanceName | $('Info').item.json.instancia |  |
| 1. Atendente.V2.0 | Resetar status | $.parameters.remoteJid | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Gerar áudio | $.parameters.bodyParameters.parameters[0].value | $json.text | json:$json |
| 1. Atendente.V2.0 | Formatar SSML | $.parameters.text | $('Atendente').item.json.output |  |
| 1. Atendente.V2.0 | Tipo de mensagem1 | $.parameters.rules.values[0].conditions.conditions[0].leftValue | $('Atendente').item.json.output |  |
| 1. Atendente.V2.0 | Tipo de mensagem1 | $.parameters.rules.values[1].conditions.conditions[0].leftValue | $('Info').item.json.mensagem_de_audio |  |
| 1. Atendente.V2.0 | Memory | $.parameters.sessionKey | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Escalar humano | $.parameters.chatId | $('Info').item.json.telegram_chat_id |  |
| 1. Atendente.V2.0 | Escalar humano | $.parameters.text | /*n8n-auto-generated-fromAI-override*/ $fromAI('Text', ``, 'string') |  |
| 1. Atendente.V2.0 | Responder mensagem áudio | $.parameters.instanceName | $('Info').item.json.instancia |  |
| 1. Atendente.V2.0 | Responder mensagem áudio | $.parameters.remoteJid | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Responder mensagem áudio | $.parameters.media | $('Converter áudio para base64').item.json.data |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.telefone | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.mensagem | $('Info').item.json.mensagem |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.timestamp | $('Info').item.json.timestamp.toDateTime('s') |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.id_mensagem | $('Info').item.json.id_mensagem |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.client_id | "06a81600-26fc-472b-880e-e6293943354e" |  |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.trace_id | $json.trace_id | json:$json |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.message_id | $json.id_mensagem | json:$json |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.remote_jid | $json.remote_jid | json:$json |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.message_type | $json.message_type | json:$json |
| 1. Atendente.V2.0 | Enfileirar mensagem. | $.parameters.columns.value.status | "pending" |  |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[0].value | $json.body.data.key.id | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[1].value | (p => p ? (p.startsWith('55') ? p : '55' + p) : null)(     (       $json.body?.data?.key?.senderPn ??       $json.body?.data?.key?.remoteJid ??       $json.body?.data?.key?.senderLid ?? ''     ).split('@')[0].replace(/\D/g,'')   ) | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[2].value | $json.body.instance | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[3].value | $json.body.data.message.conversation \|\| '' | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[4].value | $json.body.data.message.audioMessage?.ptt \|\| false | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[5].value | $json.body.data.messageTimestamp | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[6].value | $json.body.data.key.fromMe | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[7].value | $json.body.data.key.remoteJid.split('@').last() === 'g.us' | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[8].value | $json.body.server_url | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[10].value | new Date(($json.body.data.messageTimestamp\|\|0)*1000).toISOString() | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[11].value | $json.body.data.key.remoteJid | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[12].value | $json.body.data.message?.audioMessage ? 'audio' : ($json.body.data.message?.conversation ? 'text' : 'other') | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[13].value | $json.body.data.message?.audioMessage?.ptt \|\| false | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[14].value | $json.body.data.message?.audioMessage?.mimetype \|\| '' | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[15].value | $json.body.data.message?.audioMessage?.fileLength \|\| 0 | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[16].value | ($json.body.data.key.id\|\|'') + '-' + ($json.body.data.messageTimestamp\|\|0) | json:$json |
| 1. Atendente.V2.0 | Info | $.parameters.assignments.assignments[20].value | $json.body.data.message.audioMessage.url | json:$json |
| 1. Atendente.V2.0 | Atendente | $.parameters.text | $json.mensagem | json:$json |
| 1. Atendente.V2.0 | Atendente | $.parameters.text | $json.telefone | json:$json |
| 1. Atendente.V2.0 | Atendente | $.parameters.text | $json.horario | json:$json |
| 1. Atendente.V2.0 | Atendente | $.parameters.options.systemMessage | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Atendente | $.parameters.options.systemMessage | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[0].value | $fromAI("session_id", "ID da conversa", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[1].value | $fromAI("nome", "nome do cliente", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[2].value | $fromAI("telefone", "telefone", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[3].value | $fromAI("rua", "rua", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[4].value | $fromAI("itens", "intens", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[5].value | $fromAI("complemento", "complemento", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[6].value | $fromAI("pagamento", "pagamento", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[7].value | $fromAI("total", "total", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[8].value | $fromAI("cep", "cep", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[9].value | $fromAI("numero", "numero", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[10].value | $fromAI("bairro", "bairro", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[11].value | $fromAI("tipo_entrega", "tipo_entrega", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[12].value | $fromAI("cidade", "cidade", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[13].value | $fromAI("taxa_entrega", "taxa_entrega", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[14].value | $fromAI("troco_para", "troco_para", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[15].value | $fromAI("desconto", "desconto", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[16].value | $fromAI("adicionais", "adicionais", "string") |  |
| 1. Atendente.V2.0 | enviar_pedido | $.parameters.bodyParameters.parameters[17].value | $fromAI("pdv", "pdv", "string") |  |
| 1. Atendente.V2.0 | maps | $.parameters.queryParameters.parameters[0].value | $fromAI('parameters0_Value', ``, 'string') |  |
| 1. Atendente.V2.0 | cancelar_pedido | $.parameters.bodyParameters.parameters[0].value | /*n8n-auto-generated-fromAI-override*/ $fromAI('parameters0_Value', ``, 'string') |  |
| 1. Atendente.V2.0 | cancelar_pedido | $.parameters.bodyParameters.parameters[1].value | /*n8n-auto-generated-fromAI-override*/ $fromAI('parameters1_Value', ``, 'string') |  |
| 1. Atendente.V2.0 | HTTP Request | $.parameters.url | $('Info').item.json.url_evolution |  |
| 1. Atendente.V2.0 | HTTP Request | $.parameters.url | $('Info').item.json.instancia |  |
| 1. Atendente.V2.0 | HTTP Request | $.parameters.jsonBody | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | HTTP Request | $.parameters.jsonBody | JSON.stringify($json.mensagem).slice(1,-1) | json:$json |
| 1. Atendente.V2.0 | Concatenar mensagens1 | $.parameters.assignments.assignments[0].value | $('Transcrever áudio').item.json.text |  |
| 1. Atendente.V2.0 | Concatenar mensagens1 | $.parameters.assignments.assignments[1].value | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | HTTP Request1 | $.parameters.url | $json.url_evolution | json:$json |
| 1. Atendente.V2.0 | HTTP Request1 | $.parameters.url | $json.instancia | json:$json |
| 1. Atendente.V2.0 | HTTP Request1 | $.parameters.jsonBody | $json.id_mensagem | json:$json |
| 1. Atendente.V2.0 | HTTP Request2 | $.parameters.url | $json.url_evolution | json:$json |
| 1. Atendente.V2.0 | HTTP Request2 | $.parameters.url | $json.instancia | json:$json |
| 1. Atendente.V2.0 | HTTP Request2 | $.parameters.jsonBody | $json.url_audio | json:$json |
| 1. Atendente.V2.0 | historico | $.parameters.options.queryReplacement | /*n8n-auto-generated-fromAI-override*/ $fromAI('Query_Parameters', ``, 'string') |  |
| 1. Atendente.V2.0 | Marcar como lida texto | $.parameters.instanceName | $('Info').item.json.instancia |  |
| 1. Atendente.V2.0 | Marcar como lida texto | $.parameters.remoteJid | $('Info').item.json.telefone |  |
| 1. Atendente.V2.0 | Marcar como lida texto | $.parameters.messageId | $('Info').item.json.id_mensagem |  |
| 1. Atendente.V2.0 | Marcar como lida texto | $.parameters.fromMe | $('Info').item.json.fromMe |  |
| 1. Atendente.V2.0 | controle atendimentos | $.parameters.query | $("Info").first().json.telefone \|\| $json.session_id | json:$json |
| 1. Atendente.V2.0 | controle atendimentos | $.parameters.query | $("Mensagem encavalada?").all().map(i => i.json.mensagem).join("\\n") |  |
| 1. Atendente.V2.0 | atualiza atendimento | $.parameters.query | $("Info").first().json.telefone \|\| $json.session_id | json:$json |
| 1. Atendente.V2.0 | atualiza atendimento | $.parameters.query | $json.output \|\| $json.text \|\| $json.reply | json:$json |
| 1. Atendente.V2.0 | Marcar como lida audio | $.parameters.instanceName | $('Info').item.json.instancia |  |
| 1. Atendente.V2.0 | Marcar como lida audio | $.parameters.remoteJid | $('Mensagem recebida').item.json.body.data.key.remoteJid |  |
| 1. Atendente.V2.0 | Marcar como lida audio | $.parameters.messageId | $('Info').item.json.id_mensagem |  |
| 1. Atendente.V2.0 | Marcar como lida audio | $.parameters.fromMe | $('Info').item.json.fromMe |  |
| 1. Atendente.V2.0 | controle atendimentos1 | $.parameters.query | $('Info').item.json.telefone \|\| $json.session_id | json:$json |
| 1. Atendente.V2.0 | controle atendimentos1 | $.parameters.query | $json.text | json:$json |
