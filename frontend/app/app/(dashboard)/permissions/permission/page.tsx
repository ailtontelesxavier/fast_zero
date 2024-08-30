"use client";

import { CardContent } from "@/components/CardContent";
import PageTitle from "@/components/PageTitle";
import api from "@/lib/api";
import { useEffect, useState } from "react";
import AlertDialogComp from "@/components/AlertDialog";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";
import FormPermission from "../_components/FormPermission";
import ComboboxModule from "../_components/ComboboxModule";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { SearchIcon } from "lucide-react";

export default function PermissonView() {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [permissions, setPermissions] = useState<any>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState<number>(1);
  const [isBusca, setIsBusca] = useState(true);
  let [filterModulo] = useState({module:{id:0, title:''}})

  useEffect(() => {
    console.log(filterModulo)

    if (isBusca) obterPermissions();

    setIsBusca(false);

    async function obterPermissions() {
      await api
        .get(`/permissoes/permission/?module=${filterModulo.module.id}&page=${page}&page_size=10`)
        .then((response) => {
          setPermissions(response.data.permissions);
          setTotal(response.data.total_records);
        });
    }
  }, [page, isBusca, filterModulo]);

  async function deletePermission(id: number) {
    try {
      await api
        .delete("/permissoes/permission/" + id)
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Excluido com sucesso");
            setIsBusca(true);
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  function filtrar() {
    console.log(filterModulo)
    setIsBusca(true);
  }

  return (
    <div className="grid w-full">
      <PageTitle title="Cadastro de Permissao" />
      <section className="mt-3 transition-all p-2 rounded-md w-1/2">
        <CardContent className="min-w-80 md:w-[450px]">
          <div className="flex flex-row justify-between">
            <h3>Permissões</h3>
            <div>
              <FormPermission setIsBusca={setIsBusca} id={0} />
            </div>
          </div>
          <div>
            <Label>Filtro por Modulo</Label>
            <div className="flex gap-2">
              <ComboboxModule objeto={filterModulo} />
              <Button onClick={() => filtrar()} variant={"outline"} title="busca">
                <SearchIcon className="h-4 w-4"/>
              </Button>
            </div>
          </div>
          <table className="hidden md:block w-full">
            <thead className="bg-gray-50 border-b-2 border-gray-200">
              <tr>
                <th className="w-20 p-3 text-sm font-semibold tracking-wide text-left">
                  ID
                </th>
                <th className="p-3 text-sm font-semibold tracking-wide text-left">
                  NOME
                </th>
                <th className="p-3 text-sm font-semibold tracking-wide text-left">
                  MODULO
                </th>
                <th className="p-3 text-sm font-semibold tracking-wide text-left"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {permissions.map((permission: any, i: number) => (
                <>
                  {i % 2 === 0 ? (
                    <tr key={i} className="bg-white">
                      <td className="p-3 text-sm text-gray-700 hover:cursor-pointer whitespace-nowrap">
                        <span className="font-bold text-blue-500 ">
                          {permission.id}
                        </span>
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        {permission.name}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        {permission.module.title}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        <div className="flex gap-2">
                          <FormPermission setIsBusca={setIsBusca} id={permission.id} />
                          <AlertDialogComp
                            title="Tem certeza que deseja excluir?"
                            description=""
                            param={permission.id}
                            acao={deletePermission}
                          />
                        </div>
                      </td>
                    </tr>
                  ) : (
                    <tr key={i} className="bg-gray-50">
                      <td className="p-3 text-sm text-gray-700 hover:cursor-pointer whitespace-nowrap">
                        <span className="font-bold text-blue-500 hover:underline">
                          {permission.id}
                        </span>
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        {permission.name}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                      {permission.module.title}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        <div className="flex gap-2">
                          <FormPermission setIsBusca={setIsBusca} id={permission.id} />
                          <AlertDialogComp
                            title="Tem certeza que deseja excluir?"
                            description=""
                            param={permission.id}
                            acao={deletePermission}
                          />
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden">
            {permissions &&
              permissions.map((data: any) => (
                <>
                  <div className="bg-white space-y-3 p-4 rounded-lg shadow">
                    <div className="flex items-center space-x-2 text-sm">
                      <div>
                        <a
                          href="#"
                          className="text-blue-500 font-bold hover:underline"
                        >
                          {data.id}
                        </a>
                      </div>
                    </div>
                    <div className="text-sm text-gray-700">{data.name}</div>
                    <div className="flex gap-2">
                      <FormPermission setIsBusca={setIsBusca} id={data.id} />
                      <AlertDialogComp
                        title="Tem certeza que deseja excluir?"
                        description=""
                        param={data.id}
                        acao={deletePermission}
                      />
                    </div>
                  </div>
                </>
              ))}
          </div>
          <section className="w-full">
            {success && (
              <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
            )}
            {error && (
              <AlertDestructive setError={setError}>{error}</AlertDestructive>
            )}
          </section>
        </CardContent>
      </section>
    </div>
  );
}
