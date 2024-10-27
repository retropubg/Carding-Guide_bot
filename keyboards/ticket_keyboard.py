from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_ticket_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍ Create Ticket", callback_data="create_ticket"),
                InlineKeyboardButton(text="👀 View Tickets", callback_data="view_tickets")
            ],
            [
                InlineKeyboardButton(text="❌ Close Ticket", callback_data="close_ticket"),
                InlineKeyboardButton(text="🔁 Reopen Ticket", callback_data="reopen_ticket")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard

def create_ticket_options_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ General Inquiry", callback_data="ticket_general_inquiry")],
            [InlineKeyboardButton(text="💸 Sales Inquiry", callback_data="ticket_sales_inquiry")],
            [InlineKeyboardButton(text="🙏 Request Inquiry", callback_data="ticket_request_inquiry")],
            [InlineKeyboardButton(text="🔙 Back To Menu", callback_data="back_to_ticket_menu")]
        ]
    )
    return keyboard

def get_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm", callback_data="confirm"),
         InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ])
    return keyboard

def get_confirm_edit_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_ticket"),
            InlineKeyboardButton(text="🛠 Edit", callback_data="edit_ticket"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_ticket")
        ]
    ])