"use client";

import { useState, useMemo, useEffect } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { FastForward } from "lucide-react";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";
import api from "@/lib/api";
import AlertDialogComp from "@/components/AlertDialog";
import ComboboxUser from "../_components/ComboboxUser";
import ComboboxPerfil from "../_components/ComboboxPerfil";
import { PaginationActionsApi } from "@/components/paginationActionsApi";

export default function GestaoPermissaoUser() {
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState<number>(1);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState({ id: 0, username: "", email: '' });
  const [perfil, setPerfil] = useState({ id: 0 });
  const [perfilList, setPerfilList] = useState<any>();

  useEffect(() => {
    console.log(user);
    setUser(user);

    if (user.id > 0) getPerfis();

  }, [user]);

  async function addPerfil() {
    console.log(perfil);
    console.log(user);
    try {
      setLoading(true);
      await api
        .post("/users/user-role", {
          user_id: user.id,
          role_id: perfil.id,
        })
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Cadastrado com sucesso");
            getPerfis();
          }
        })
        .catch((error) => {
          //console.log(JSON.parse(error.request.response).detail)
           if (error.response.status === 400) {
            setError("Já cadastrado");
            return;
          }
          const responseObject = JSON.parse(error.request.response)
          setError(responseObject.detail)
        });
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    } finally {
      setLoading(false);
    }
  }

  async function getPerfis() {
    try {
      setLoading(true);
      console.log(user.id)
      await api
        .get(`/users/user-role/${user.id}?page=${page}&page_size=10`)
        .then((response) => {
          console.log(response.data);
          setPerfilList(response.data);
          setTotal(response.data.total_records)
        }).catch((error) => {
          const responseObject = JSON.parse(error.request.response)
          setError(responseObject.detail)
        });
    } catch (error:any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    } finally {
      setLoading(false);
    }
  }
  async function deleteRoleUser(obj: any) {
    try {
      console.log(perfil.id)
      console.log(obj.id)
      await api
        .delete(`/users/user-role/?user_role_id=${obj.id}`)
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Excluido com sucesso");
            getPerfis();
          }
        })
        .catch((error) => {
          const responseObject = JSON.parse(error.request.response)
          setError(responseObject.detail)
        });
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  function limpar() {
    setUser({ id: 0, name: "", roles: [] });
    setPerfil({ id: 0 });
    setPerfilList({ rows: [] });
    setPage(1);
  }

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Gerenciar Perfil por Usuario</CardTitle>
        <CardDescription>
          Configura perfis por usuario.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Label htmlFor="profile">Selecione um Usuario</Label>
            <ComboboxUser setObjet={setUser} objeto={user} />
          </div>
          <div>
            <Label htmlFor="search">Adicionar Perfil</Label>
            <div className="flex gap-2">
              <ComboboxPerfil setObjet={setPerfil} objeto={perfil} />
              <Button
                title="Adicionar Perfil"
                disabled={user.id <= 0 || perfil.length <= 0}
                onClick={() => addPerfil()}
              >
                <FastForward className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
        <Separator className="my-6" />
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Perfil</TableHead>
              <TableHead></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {console.log(perfilList)}
            {perfilList?.rows.map((perfil) => (
              <TableRow key={perfil.id}>
                <TableCell className="font-medium">{perfil.id}</TableCell>
                <TableCell className="font-medium">
                  {perfil.role.name}
                </TableCell>
                <TableCell className="text-right">
                  <AlertDialogComp
                    title="Tem certeza que deseja excluir?"
                    description=""
                    param={perfil}
                    acao={deleteRoleUser}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <section>
          <PaginationActionsApi
            itensPerPage={10}
            count={total}
            setPageIndex={setPage}
            pageIndex={page}
          />
        </section>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-end justify-end">
          <Button type="button" variant={"secondary"} onClick={() => limpar()}>
            Limpar
          </Button>
        </div>
        <section className="w-full">
          {success && (
            <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
          )}
          {error && (
            <AlertDestructive setError={setError}>{error}</AlertDestructive>
          )}
        </section>
      </CardFooter>
    </Card>
  );
}
