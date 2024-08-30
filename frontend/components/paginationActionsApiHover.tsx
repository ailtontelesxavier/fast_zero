"use client";
import { cn } from "@/lib/utils";
import React, { useState } from "react";

interface PaginationActionsApiProps {
  itensPerPage: number;
  count: number;
  setPageIndex: Function;
  pageIndex: number;
}

export function PaginationActionsApiHover({
  itensPerPage,
  count,
  setPageIndex,
  pageIndex,
}: PaginationActionsApiProps) {
  const [postsPerPage, setPostsPerPage] = useState(itensPerPage);

  var totalPosts = count;

  const next = (totalPosts / postsPerPage) < pageIndex;

  const totalPorPagina = (totalPosts / postsPerPage);

  const lastPostIndex = pageIndex * postsPerPage;
  const firstPostIndex = lastPostIndex - postsPerPage;

  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(totalPosts / postsPerPage); i++) {
    pageNumbers.push(i);
  }

  const maxPageNum = 5; // Maximum page numbers to display at once
  const pageNumLimit = Math.floor(maxPageNum / 2); // Current page should be in the middle if possible

  let activePages = pageNumbers.slice(
    Math.max(0, pageIndex - 1 - pageNumLimit),
    Math.min(pageIndex - 1 + pageNumLimit + 1, pageNumbers.length)
  );

  const renderPages = () => {
    const renderedPages = activePages.map((page, idx) => (
      <span
        key={idx}
        className={cn(
          pageIndex === page ? "rounded-md bg-neutral-100" : "",
          "border p-2 hover:cursor-pointer"
        )}
        onClick={() => {
          setPageIndex(page);
        }}
      >
        {page}
      </span>
    ));

    // Add ellipsis at the start if necessary
    if (activePages[0] > 1) {
      renderedPages.unshift(
        <span
          key="ellipsis-start"
          className={cn("border p-2 hover:cursor-pointer")}
          onClick={() => {
            setPageIndex(activePages[0] - 1);
          }}
        >
          &lt;&lt;
        </span>
      );
    }

    // Add ellipsis at the end if necessary
    if (activePages[activePages.length - 1] < pageNumbers.length) {
      renderedPages.push(
        <span
          key="ellipsis-end"
          className={cn("border p-2 hover:cursor-pointer")}
          onClick={() => {
            setPageIndex(activePages[activePages.length - 1] + 1);
          }}
        >
          &gt;&gt;
        </span>
      );
    }

    return renderedPages;
  };

  return (
    <>
      {Math.ceil(count / totalPorPagina) > 1 ? (
        <div className="mt-10 flex justify-between ">
          <div className="justify-start">
            {pageIndex > 1 ? (
              <span
                className="goup gap-2 border p-2 hover:cursor-pointer transition-colors duration-300 hover:text-slate-500"
                onMouseOver={() => {
                  setTimeout(() => {
                    setPageIndex(pageIndex - 1);
                  }, 600);
                }}
                onClick={() => {
                  setPageIndex(pageIndex - 1);
                }}
              >
                Página anterior
              </span>
            ) : (
              <div></div>
            )}
          </div>
          <div className="flex flex-col justify-center items-center ">
            <div>{renderPages()}</div>
            <span className="text-xs mt-2">
              {count
                ? `${pageIndex} de ${Math.ceil(totalPosts / postsPerPage)}`
                : ""}
            </span>
          </div>
          <div className="justify-end">
            {pageIndex < Math.ceil(totalPosts / postsPerPage) ? (
              <span
                className="goup gap-2 border p-2 hover:cursor-pointer transition-colors duration-300 hover:text-slate-500"
                onMouseOver={() => {
                  setTimeout(() => {
                    setPageIndex(pageIndex + 1);
                  }, 600);
                }}
                onClick={() => {
                  setPageIndex(pageIndex + 1);
                }}
              >
                Próxima página
              </span>
            ) : (
              <div></div>
            )}
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
}
