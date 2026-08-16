export default function CancelModal({closeModal,info}){

    const CancelHandler = async()=>{
        const token = sessionStorage.getItem("access_token");

            const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/${info.ticket_id}/cancel/`,
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    const result = await response.json();
    console.log(result);
    if(response.ok){
        alert("لغو بلیط با موفقیت انجام شد")
        closeModal()
    }
    
    
    }
    

    return(
    <div className=" wrapper fixed inset-0 z-[100] flex justify-center items-center">
        <div  onClick={closeModal} className="absolute min-h-screen inset-0 bg-black/80" />
        <div className=" h-auto w-auto bg-white rounded-xl z-[150] p-10">
            <div dir="rtl" className=" flex flex-row">
            <h1>:مبلغ خرید</h1>
            <h3>{info.purchase_price} تومان</h3>
        </div>
        <div dir="rtl" className=" flex flex-row">
            <h1>:مبلغ قابل استرداد</h1>
            <h3>{info.refund_percent} تومان</h3>
        </div>
        <div dir="rtl" className=" flex flex-row">
            <h1>:مبلغ جریمه</h1>
            <h3>{info.refund_amount} تومان</h3>
        </div>
        <div dir="rtl" className=" flex flex-row">
            <h1>: درصد استرداد</h1>
            <h3>{info.penalty_amount}</h3>
        </div>
        <button onClick={CancelHandler}>تایید کنسلی</button>
        </div>
        
    </div> 
      
    );
}