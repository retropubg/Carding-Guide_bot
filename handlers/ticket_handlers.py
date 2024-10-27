from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.ticket_keyboard import get_ticket_keyboard, create_ticket_options_keyboard
from utils.ticket_utils import generate_ticket_id, save_ticket, notify_admin
from keyboards.ticket_keyboard import *
from aiogram import types
from aiogram.types import ErrorEvent
import logging



router = Router()

class TicketStates(StatesGroup):
    WAITING_FOR_MESSAGE = State()
    CONFIRMING_SUBMISSION = State()
    WAITING_FOR_STATUS_UPDATE = State()





@router.callback_query(F.data.startswith("ticket_"))
async def handle_ticket_inquiry(callback: CallbackQuery, state: FSMContext):
    inquiry_type = callback.data.split("_")[1]
    await state.update_data(inquiry_type=inquiry_type)
    await state.set_state(TicketStates.WAITING_FOR_MESSAGE)
    
    await callback.message.edit_text(
        f"You've selected {inquiry_type.replace('_', ' ').title()} Inquiry.\n"
        "Please provide details for your inquiry:",
        reply_markup=None
    )
    logging.info(f"Set state to WAITING_FOR_MESSAGE for inquiry type: {inquiry_type}")

@router.message(TicketStates.WAITING_FOR_MESSAGE)
async def process_ticket_message(message: Message, state: FSMContext):
    logging.info(f"Received message: {message.text}")
    user_message = message.text
    await state.update_data(user_message=user_message)
    
    data = await state.get_data()
    inquiry_type = data.get('inquiry_type', 'Unknown')
    
    await message.answer(
        f"Please review your {inquiry_type.replace('_', ' ').title()} Inquiry:\n\n"
        f"Message: {user_message}\n\n"
        "Is this correct? You can confirm, edit, or cancel your submission.",
        reply_markup=get_confirm_edit_cancel_keyboard()
    )
    await state.set_state(TicketStates.CONFIRMING_SUBMISSION)
    logging.info(f"Set state to CONFIRMING_SUBMISSION. Message: {user_message}")

# Add handlers for confirm, edit, and cancel actions

@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    logging.info(f"Fallback handler triggered. Current state: {current_state}")
    await message.answer("I'm not sure how to process that message. Please try using the menu options.")

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "confirm_ticket")
async def confirm_ticket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    inquiry_type = data['inquiry_type']
    user_message = data['user_message']
    
    # Here you would typically save the ticket to your database
    # For this example, we'll just acknowledge the submission
    await callback.message.edit_text(
        f"Your {inquiry_type.replace('_', ' ').title()} Inquiry has been submitted successfully.\n"
        "Our support team will review it shortly.",
        reply_markup=None
    )
    await state.clear()

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "edit_ticket")
async def edit_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please provide the updated details for your inquiry:",
        reply_markup=None
    )
    await state.set_state(TicketStates.WAITING_FOR_MESSAGE)

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "cancel_ticket")
async def cancel_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Your ticket submission has been cancelled.",
        reply_markup=None
    )
    await state.clear()

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "confirm")
async def submit_ticket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ticket_id = data['ticket_id']
    inquiry_type = data['inquiry_type']
    user_message = data['user_message']
    
    await save_ticket(callback.from_user.id, ticket_id, inquiry_type, user_message)
    await notify_admin(ticket_id, inquiry_type, user_message)
    
    await callback.message.edit_text(
        f"Your ticket (ID: {ticket_id}) has been submitted successfully.\n"
        "An admin will review it shortly.",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "cancel")
async def cancel_submission(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Ticket submission cancelled. What would you like to do?",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()

@router.callback_query(F.data == "back_to_ticket_menu")
async def back_to_ticket_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎫 Ticket Management Menu\n\n"
        "Here you can manage all ticket-related operations:\n"
        "• Create new tickets\n"
        "• View existing tickets\n"
        "• Close resolved tickets\n"
        "• Reopen closed tickets if needed\n\n"
        "Please select an option:",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()

@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery):
    # This assumes you have a main menu implemented elsewhere
    await callback.message.edit_text(
        "Welcome to the main menu. Please select an option:",
        reply_markup=get_main_menu_keyboard()  # You'd need to implement this function
    )
