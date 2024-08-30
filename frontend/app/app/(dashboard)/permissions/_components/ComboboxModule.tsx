"use client"

import { useState, useMemo, useEffect } from "react"
import { Input } from "@/components/ui/input"
import api from "@/lib/api"

export default function ComboboxModule(
  {objeto}: {objeto:any}) {
  const [searchTerm, setSearchTerm] = useState(
    objeto.module && (objeto.module.title ?? "")
  )
  const [selectedOption, setSelectedOption] = useState(null)
  const [hasFocus, setHasFocus] = useState(false)
  const [options, setOptions] = useState([])

  useEffect(() => {

    getModel();

    async function getModel() {
      await api.get(`/permissoes/module/find/?title=`+searchTerm)
        .then(response => {
          console.log(response.data.modules)
          setOptions(response.data.modules)
        })
        .catch(error => {
          console.error("There was an error fetching the options!", error)
        })
    }
  }, [searchTerm, objeto])

  const filteredOptions = useMemo(() => {
    return options.filter((option) => option.title.toLowerCase().includes(searchTerm.toLowerCase()))
  }, [searchTerm, options])
  function handleInputChange(e:any) {
    setSearchTerm(e.target.value)
    setSelectedOption(null)
  }
  function handleOptionSelect(option:any) {
    setSelectedOption(option)
    setSearchTerm(option.title)
    objeto.module_id = option.id
    objeto.module.id = option.id
    objeto.module.title = option.title  
    setHasFocus(false)
  }

  function handleFocus() {
    setHasFocus(true)
  }
  function handleBlur (){
    setTimeout(() => {
      setHasFocus(false)
    }, 100) // Small timeout to allow click event on option before hiding
  }
  return (
    <div className="relative w-full max-w-md">
      <Input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleInputChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
        className="w-full rounded-md border border-input bg-background px-4 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
      />
      {hasFocus && filteredOptions.length > 0 && (
        <div className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md border border-card bg-card shadow-lg">
          <ul className="py-1">
            {filteredOptions.map((option) => (
              <li
                key={option.id}
                className={`cursor-pointer px-4 py-2 text-foreground hover:bg-primary hover:text-primary-foreground ${
                  selectedOption?.id === option.id ? "bg-primary text-primary-foreground" : ""
                }`}
                onMouseDown={() => handleOptionSelect(option)}
              >
                {option.title}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}