'use client';
import { AlertDestructive } from "@/components/AlertDestructive";
import { AlertSuccess } from "@/components/AlertSuccess";
import PageTitle from "@/components/PageTitle";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/lib/api";
import { format, parseISO } from "date-fns";
import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import AcoesUser from "../_components/AcoesUser";
import { QRCodeSVG } from "qrcode.react";


export default function UserFormPage({ params }: { params: { id: number } }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [is_active, setIs_active] = useState(false);
  const [created_at, setCreated_at] = useState<Date>();
  const [updated_at, setUpdated_at] = useState<Date>();
  const [otp_base32, setOtp_base32] = useState('');

  
  useEffect(() => {
    obterUser();
  }, [success]);

  async function obterUser() {
    try {
      await api.get("/users/" + params.id).then((response: any) => {
        console.log(response);
        if (response.status === 200) {
          setUsername(response.data.username);
          setEmail(response.data.email);
          setIs_active(response.data.is_active);
          setCreated_at(response.data.created_at);
          setUpdated_at(response.data.updated_at);
          setOtp_base32(response.data.qr_code);
        }
      });
    } catch (error:any) {
      if (error.response) {
        setError(error.response.data.detail + ";" + error.message);
      }
    }
  }

  async function saveUser() {
    try {
      await api
        .put("/users/update/" + params.id, {
          id: params.id,
          username: username,
          email: email,
          is_active: is_active,
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

  function handleUpdateUser(event: FormEvent) {
    event.preventDefault();
    saveUser();
  }
  function handleCheckboxChange(event: React.ChangeEvent<HTMLInputElement>) {
    setIs_active(event.target.checked);
  }
  return (
    <div className="flex flex-col gap-5 w-full">
      <PageTitle title="Cadastro de Usuario" />
      <section>
        <div className="flex w-full justify-end ">
          <AcoesUser id={params.id}/>
        </div>
        <form onSubmit={handleUpdateUser}>
          <div className="flex flex-col gap-2 md:grid grid-cols-2">
            <div className="grid grid-flow-row-dense grid-cols-3 gap-2">
              <div>
                <Label htmlFor="is_active">Ativo</Label>
                <input
                  className="peer h-4 w-4 cursor-pointer ml-5"
                  type="checkbox"
                  checked={is_active}
                  id="is_active"
                  onChange={handleCheckboxChange}
                />
              </div>
              <div className="col-span-2">
                <Label htmlFor="username">Usuario</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="Usuario"
                  required={true}
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                />
              </div>
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="text"
                placeholder="email"
                required={true}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="created_at">Criado</Label>
              <Input
                id="created_at"
                type="text"
                disabled={true}
                value={
                  created_at &&
                  format(
                    new Date(created_at).toLocaleDateString(),
                    "dd-MM-yyyy"
                  )
                }
              />
            </div>
            <div>
              <Label htmlFor="updated_at">Atualizado</Label>
              <Input
                id="updated_at"
                type="text"
                disabled={true}
                value={
                  updated_at &&
                  format(
                    new Date(updated_at).toLocaleDateString(),
                    "dd-MM-yyyy"
                  )
                }
              />
            </div>
            <div>
              <Label>OTP</Label>
              { otp_base32 && <QRCodeSVG value={otp_base32} className="h-52 w-52" />}
            </div>
          </div>
          <div className="flex mt-5 gap-4 w-full justify-end">
            <Button
              type="button"
              variant={"secondary"}
              onClick={() => router.back()}
            >
              Cancelar
            </Button>
            <Button type="submit">Atualizar</Button>
          </div>
        </form>
      </section>
      <section>
        {success && (
          <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
        )}
        {error && (
          <AlertDestructive setError={setError}>{error}</AlertDestructive>
        )}
      </section>
    </div>
  );
}
