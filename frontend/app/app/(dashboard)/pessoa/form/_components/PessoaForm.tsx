import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function PessoaForm() {
  const [tipoRegistro, setTipoRegistro] = useState("fisica")

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Cadastro de Pessoa</CardTitle>
      </CardHeader>
      <CardContent>
        <form className="space-y-6">
          <RadioGroup
            defaultValue="fisica"
            onValueChange={setTipoRegistro}
            className="flex space-x-4"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="fisica" id="fisica" />
              <Label htmlFor="fisica">Pessoa Física</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="juridica" id="juridica" />
              <Label htmlFor="juridica">Pessoa Jurídica</Label>
            </div>
          </RadioGroup>

          {tipoRegistro === "fisica" ? (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="nome">Nome</Label>
                <Input id="nome" placeholder="Nome completo" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cpf">CPF</Label>
                <Input id="cpf" placeholder="000.000.000-00" />
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="razaoSocial">Razão Social</Label>
                <Input id="razaoSocial" placeholder="Razão Social" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cnpj">CNPJ</Label>
                <Input id="cnpj" placeholder="00.000.000/0000-00" />
              </div>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="email">E-mail</Label>
            <Input id="email" type="email" placeholder="exemplo@email.com" />
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Endereço</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="cep">CEP</Label>
                <Input id="cep" placeholder="00000-000" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="estado">Estado</Label>
                <Select>
                  <SelectTrigger id="estado">
                    <SelectValue placeholder="Selecione o estado" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="sp">São Paulo</SelectItem>
                    <SelectItem value="rj">Rio de Janeiro</SelectItem>
                    <SelectItem value="mg">Minas Gerais</SelectItem>
                    {/* Add more states as needed */}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="cidade">Cidade</Label>
              <Input id="cidade" placeholder="Cidade" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="rua">Rua</Label>
                <Input id="rua" placeholder="Nome da rua" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="numero">Número</Label>
                <Input id="numero" placeholder="Número" />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="complemento">Complemento</Label>
              <Input id="complemento" placeholder="Apartamento, sala, etc." />
            </div>
          </div>

          <Button type="submit" className="w-full">Cadastrar</Button>
        </form>
      </CardContent>
    </Card>
  )
}