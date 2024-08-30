import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

export default function Component() {
  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Cadastro de Negociação</CardTitle>
        <CardDescription>Preencha os dados da negociação.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="processo">Número do Processo</Label>
            <Input id="processo" placeholder="Informe o número do processo" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="contrato">Contrato</Label>
            <Input id="contrato" placeholder="Informe o contrato" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="executado">Executado</Label>
            <Checkbox id="executado" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="tipo-acordo">Tipo de Acordo</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o tipo de acordo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="homologacao">Homologação</SelectItem>
                <SelectItem value="termo-acordo">Termo de Acordo</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="observacao">Observação</Label>
          <Textarea id="observacao" placeholder="Informe a observação" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="status">Status</Label>
          <Select id="status">
            <SelectTrigger>
              <SelectValue placeholder="Selecione o status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="liquido">Líquido</SelectItem>
              <SelectItem value="descumprido">Descumprido</SelectItem>
              <SelectItem value="retorno-execucao">Retorno à Execução</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button type="submit">Salvar</Button>
      </CardFooter>
    </Card>
  )
}