export default function SearchFillter(){
    return(
        <div>
            <div className=" h-30 bg-blue-950 text-white  mt-25 flex flex-wrap flex-row-reverse justify-around p-2 items-center rounded-xl">
            <input className=" text-white border-2 p-2 rounded-md" type="text" dir="rtl" placeholder="نام تیم"></input>
            <select>
                <label>ورزش</label>
                <option value="">همه ورزش ها</option>
                <option value="footbal">فوتبال</option>
                <option value="volleyball">والیبال</option>
                <option value="basketball">بسکتبال</option>
            </select>
            <select>
            <label>ورزشگاه</label>
                <option value="">همه ورزشگاه ها</option>
            </select>
             <select>
            <label>شهر</label>
                <option>انتخاب شهر</option>
            </select>
         
            
            <input dir="rtl" className=" text-right" type="date"></input>
            <button className=" text-black flex w-30 items-center justify-center bg-[#52D15C] p-3 rounded-lg">
            جستجو
            <svg className=" w-5 m-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.323 13.383a5.5 5.5 0 1 1 1.06-1.06l2.897 2.897a.75.75 0 1 1-1.06 1.06l-2.897-2.897Zm.677-4.383a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z"/></svg>
          </button>
         </div>
         
    
        </div>
       
    )
}