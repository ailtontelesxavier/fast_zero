/**
 * eslint-disable @next/next/no-img-element
 *
 * @format
 */

/** @format */
"use client";

import { DataTable } from "@/components/DataTable";
import { ColumnDef } from "@tanstack/react-table";
import React, { useEffect, useState } from "react";
import PageTitle from "@/components/PageTitle";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";
import { Icons } from "@/components/icons";
import { CheckIcon, Cross2Icon } from "@radix-ui/react-icons";
import api from "@/lib/api";
import { useRouter } from "next/navigation";
import { PaginationActionsApi } from "@/components/paginationActionsApi";

type Props = {};
type UserType = {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
};



export default function UsersPage({ }: Props) {
  const router = useRouter();
  const [users, setUsers] = useState<any>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState<number>(1);
  const [isSubmit, setIsSubmit] = useState<boolean>(false);

  const columns: ColumnDef<UserType>[] = [
    {
      accessorKey: "id",
      header: "ID",
      cell: ({ row }) => {
        return (
          <div className="flex gap-2 items-center hover:cursor-pointer hover:text-blue-500"
            onClick={() => router.push(`/app/users/form/${row.getValue("id")}`)}
          >
            <p>{row.getValue("id")} </p>
          </div>
        );
      },
    },
    {
      accessorKey: "username",
      header: "Login",
    },
    {
      accessorKey: "email",
      header: "Email",
    },
    {
      accessorKey: "is_active",
      header: "Ativo",
      cell: ({ row }) => {
        return (
          <>{row.getValue("is_active") ? <CheckIcon className="h-4 w-4" /> : <Cross2Icon className="h-4 w-4" />}</>
        );
      },
    },
  ];

  useEffect(() => {
    obterUsers();
    async function obterUsers() {
      await api.get(`/users/?page=${page}&page_size=10`).then((response) => {
        setUsers(response.data.users)
        setTotal(response.data.total_records)
      })
    }
  }, [page]);


  return (
    <div className="flex flex-col gap-5  w-full">
      <PageTitle title="Users" />
      <div className="flex flex-1 w-full justify-end items-end">
        <Button
          variant="outline"
          size="sm"
          className="rounded-full space-x-2 mt-2"
          onClick={() => {
            setIsSubmit(true);
            router.push("/app/users/form");
          }}
        >
          {isSubmit ? (
            <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            ""
          )}{" "}
          <span>Adicionar Negociação</span>
          <PlusIcon className="h-4 w-4" />
        </Button>
      </div>
      <section className="hidden md:block">
        <DataTable columns={columns} data={users} />
      </section>
      <section className="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden">
        {users && users.map((data: any) => (
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
                <div className="text-gray-500">{data.username}</div>
                <div>
                  <span className="p-1.5 text-xs font-medium uppercase tracking-wider text-green-800 bg-green-200 rounded-lg bg-opacity-50">
                    Delivered
                  </span>
                </div>
              </div>
              <div className="text-sm text-gray-700">
                {data.email}
              </div>
              <div className="text-sm font-medium text-black">$200.00</div>
            </div>
          </>
        ))}
      </section>
      <section>
        <PaginationActionsApi
          itensPerPage={10}
          count={total}
          setPageIndex={setPage}
          pageIndex={page}
        />
      </section>
    </div>
  );
}
