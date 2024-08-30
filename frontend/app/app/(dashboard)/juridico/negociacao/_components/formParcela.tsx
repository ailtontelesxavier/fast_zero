import { AlertDestructive } from "@/components/AlertDestructive";
import { useRouter } from "next/navigation";
import { AlertSuccess } from "@/components/AlertSuccess";
import InputDateForm from "@/components/input-data-form";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import api from "@/lib/api";
import { EraserIcon, Pencil2Icon } from "@radix-ui/react-icons";
import { PlusIcon } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

export default function FormParcela({
  id,
  negociacao_id,
  setIsBusca,
}: {
  id: number;
  negociacao_id: number;
  setIsBusca: Function;
}) {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [parcela, setParcela] = useState<any>({negociacao_id:negociacao_id});
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [busca, setBusca] = useState(true);

  const router = useRouter();

  useEffect(() => {
    setParcela({
      ...parcela,
      type: parcela?.type ? ''+parcela?.type : '1',
      negociacao_id:negociacao_id,
      is_val_juros: parcela?.is_val_juros ?? false
    });
    
    if (!modalIsOpen) {
      // busca perfils ao fechar modal
      setIsBusca(true);
      return;
    }

    if (id) {
      if(busca) getParcela();
    }
    setBusca(false);

    async function getParcela() {
      await api.get(`/juridico/parcelamento/${id}`).then((response) => {
        console.log(response);
        setParcela({...response.data});
        console.log(parcela?.data)
      });
    }
  }, [id, modalIsOpen, busca, parcela?.type, parcela?.data]);

  function closeModal() {
    setParcela({negociacao_id:negociacao_id})
    setIsBusca(true);
    setBusca(true);
    setError("");
    setSuccess('');
    setModalIsOpen(false);
  }

  function setOpenChange(open: boolean) {
    setParcela({negociacao_id:negociacao_id});
    setBusca(true);
    setModalIsOpen(open)
  }

  function handleParcela(event: FormEvent) {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement)

    var isValJuros = true

    console.log(formData)
    console.log(negociacao_id)
    console.log(formData.get('is_val_juros'))
    if (formData.get('is_val_juros') == null){
      isValJuros = false
    }
    setParcela({
      ...parcela,
      negociacao_id: negociacao_id,
      type:formData.get('type'),
      val_pago:formData.get('val_pago'),
      obs_val_pago:formData.get('obs_val_pago'),
      data_pgto:!(formData.get('data_pgto') as String).trim() ? null : parcela?.data_pgto,
      is_val_juros: isValJuros
    })

    if (id > 0) {
      updateParcela();
      setIsBusca(true);
      setError("");
      return;
    }
    createParcela();
    setIsBusca(true);
    setError("");
  }
  function handleForm(event: FormEvent) {
    event.preventDefault();
  }

  async function createParcela() {
    try {
      await api
        .post("/juridico/parcelamento", {
          ...parcela,
        })
        .then((response: any) => {
          if (response.status === 201) {
            setSuccess("Cadastrado com sucesso");
          }
        })
        .catch((error) => {
          if (error.response.status === 409) {
            setError("Já cadastrado");
          }
          const responseObject = JSON.parse(error.request.response)
          var errors = ''
          responseObject.detail.forEach((val: any) => {
            errors += (`(Campo: ${val.loc[1]} Erro: ${val.msg}) `)
          });
          setError("Error interno: " + errors)
        });
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  async function updateParcela() {
    try {
      await api
        .patch("/juridico/parcelamento/" + parcela.id, {
          ...parcela,
        })
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Atualizado com sucesso");
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }
  return (
    <div className="w-full flex justify-end">
      <Card>
        <Dialog open={modalIsOpen} onOpenChange={setOpenChange}>
          <DialogTrigger asChild>
            <Button
              variant="outline"
              type="button"
              size="sm"
              title={id ? "Editar" : "Adicionar Parcela"}
              onClick={() => setModalIsOpen(true)}
            >
              {id ? (
                <Pencil2Icon className="h-4 w-4" />
              ) : (
                <PlusIcon className="h-4 w-4" />
              )}
            </Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Cadastro de Parcela</DialogTitle>
              <DialogDescription></DialogDescription>
            </DialogHeader>

            <form onSubmit={handleParcela}>
              <div className="grid gap-4 py-2">

                {/* ID and Tipo */}
                <div className="grid grid-flow-col gap-1 m-1 items-start justify-start">
                  {id > 0 && (
                    <div className="flex flex-col w-36 justify-start items-start space-y-2">
                      <Label>ID:</Label>
                      <Input disabled value={parcela.id ?? ""} />
                    </div>
                  )}
                </div>
                <div className="grid grid-flow-col m-2 justify-start items-start space-x-1">
                  <div className="flex flex-col w-36 justify-start items-start space-y-2">
                    <Label>Parcela</Label>
                    <Input
                      type="number"
                      name="numero_parcela"
                      required
                      min={0}
                      value={parcela.numero_parcela}
                      onChange={(value) => {
                        setParcela({
                          ...parcela,
                          numero_parcela: parseInt(value.target.value)
                        })
                      }}
                    />
                  </div>
                  <div className="flex flex-col w-36 justify-start items-start space-y-2">
                    <Label htmlFor="tipo-acordo">Tipo</Label>
                    <Select
                      name="type"
                      value={parcela?.type}
                      onValueChange={(value) => {
                        setParcela({
                          ...parcela,
                          type: ''+value,
                        });
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione um tipo" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">Contrato</SelectItem>
                        <SelectItem value="2">Entrada</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Data and Data Pagamento */}
                <div className="grid grid-flow-col m-2 justify-start items-start space-x-1">
                  <div className="flex flex-col space-y-2">
                    <Label>Data</Label>
                    <InputDateForm
                      field={parcela?.data}
                      onClickDay={handleChangeData}
                    />
                    <input hidden={true} name="data" value={parcela?.data ?? null} />
                  </div>
                  <div className="flex flex-col space-y-2">
                    <Label>Data Pagamento</Label>
                    <div className="flex gap-2">
                      <InputDateForm
                        field={parcela?.data_pgto}
                        onClickDay={handleChangeDataPgto}
                      />
                      <span className="text-muted-foreground gap-9 cursor-pointer">
                        {parcela?.data_pgto && (
                          <EraserIcon
                            onClick={handleClear}
                            className="ml-auto h-5 w-5 opacity-50 text-muted-foreground cursor-pointer"
                          />
                        )}
                      </span>
                    </div>
                    <input hidden={true} name="data_pgto" value={parcela?.data_pgto ?? null} />
                  </div>
                </div>

                {/* Valor Parcela and Primeira Parcela */}
                <div className="grid grid-flow-col gap-1 m-2 items-start justify-start">
                  <div className="flex flex-col items-start space-y-2 w-36">
                    <Label htmlFor="val_parcela">Valor Parcela</Label>
                    <Input
                      id="val_parcela"
                      type="number"
                      required
                      step="0.01"
                      min="0"
                      value={parcela?.val_parcela}
                      onChange={(e) => {
                        setParcela({
                          ...parcela,
                          val_parcela: e.target.value,
                        });
                      }}
                    />
                  </div>
                  <div className="flex flex-col items-start space-y-2 w-36">
                    <Label htmlFor="val_pago">Valor Recebido</Label>
                    <Input
                      id="val_pago"
                      type="number"
                      step="0.01"
                      min="0"
                      value={parcela?.val_pago}
                      onChange={(e) => {
                        setParcela({
                          ...parcela,
                          val_pago: e.target.value,
                        });
                      }}
                    />
                  </div>
                </div>

                {/* Juros */}
                <div className="grid grid-flow-col gap-1 m-2 items-start justify-start">
                  <div className="space-y-2 gap-4">
                    <Checkbox
                      id="jurus"
                      name="is_val_juros"
                      checked={parcela?.is_val_juros ?? false}
                      onCheckedChange={(value: boolean) => {
                        setParcela({
                          ...parcela,
                          is_val_juros: value
                        })
                      }}
                    />
                    <Label htmlFor="jurus">Juros</Label>
                  </div>
                </div>

                {/* Observações */}
                <div className="grid grid-flow-col gap-1 m-2 items-start justify-start">
                  <div className="space-y-2 gap-2">
                    <Label htmlFor="observacoes">Obs.</Label>
                    <Textarea
                      className="w-96"
                      name="obs_val_pago"
                      value={parcela?.obs_val_pago}
                      onChange={(e) => {
                        setParcela({
                          ...parcela,
                          obs_val_pago: e.target.value
                        })
                      }}
                    />
                  </div>
                </div>

              </div>

              {/* Botões de Ação */}
              <div className="flex items-end justify-end gap-2">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => closeModal()}
                >
                  Cancelar
                </Button>
                <Button type="submit">Salvar</Button>
              </div>
            </form>

            {/* Alerta de Sucesso ou Erro */}
            <DialogFooter className="w-full">
              <section className="w-full">
                {success && (
                  <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
                )}
                {error && (
                  <AlertDestructive setError={setError}>{error}</AlertDestructive>
                )}
              </section>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </Card>
    </div>

  );

  function handleChangeData(value: any) {
    setParcela({
      ...parcela,
      data: value.toISOString().substring(0, 10) ?? null,
    });
  }
  function handleChangeDataPgto(value: any) {
    console.log(typeof value)
    setParcela({
      ...parcela,
      data: parcela.data,
      data_pgto: value.toISOString().substring(0, 10) ?? null,
    });
  }

  function handleClear() {
    setParcela({
      ...parcela,
      data_pgto: null
    })
  };
}
