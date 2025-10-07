# Código

| workflow | node | param_key | loc | excerpt |
| --- | --- | --- | --- | --- |
| 1. Atendente.V2.0 | Mensagem encavalada? | jsCode | 10 | const ultima_mensagem_da_fila = $input.last() const mensagem_do_workflow = $('Info').first()  if (ultima_mensagem_da_fila.json.id_mensagem !== mensagem_do_workflow.json.id_mensagem) {   // Mensagem encavalada, para o workflow   return []; }  // Pass-through da fila de mensagens return $input.all(); |
| 1. Atendente.V2.0 | Code | jsCode | 29 | // Prioriza o texto do node "Atendente" const fromAttNode =   ($node["Atendente"]?.json?.output) ??   ($items("Atendente")?.[0]?.json?.output);  // Demais fontes (fallbacks) const raw =   fromAttNode ??   $json?.message?.content ??   $json?.output ??   $json?.mensagem ??   $json?.text ??   $json?.texto ??   "";  // Normaliza p/ string const texto = String(raw \|\| "").trim();  // Se vazio, não quebr... |
