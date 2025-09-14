from decimal import Decimal


def build_payment_email(
    owner_name: str,
    owner_email: str,
    amount: Decimal,
    collect_name: str
) -> tuple[str, str, list[str], str]:
    recipient_list = [owner_email,]
    subject = f"Вы произвели оплату сбора - {collect_name}"
    message = (
        f"Здравствуйте {owner_name}!\n\n"
        f"Вы успешно произвели оплату сбора {collect_name} суммой {amount}.\n\n"
    )
    html_message = (
        f"<h3>Здравствуйте {owner_name}!</h3>"
        f"<p>Вы успешно произвели оплату сбора {collect_name} суммой {amount}.</p>"
    )

    return subject, message, recipient_list, html_message


def build_collect_email(
    author_name: str,
    author_email: str,
    planned_amount: Decimal,
    collect_name: str
) -> tuple[str, str, list[str], str]:
    recipient_list = [author_email,]
    subject = f"Вы создали сбор - {collect_name}"
    message = (
        f"Здравствуйте {author_name}!\n\n"
        f"Вы успешно создали сбор - {collect_name}.\n\n"
        f"Планируемая сумма сбора: {planned_amount}.\n\n"
        f"Дата завершения сбора: {planned_amount}.\n\n"
    )
    html_message = (
        f"<h3>Здравствуйте {author_name}!<h3>"
        f"<p>Вы успешно создали сбор - {collect_name}.</p>"
        f"<p>Планируемая сумма сбора: {planned_amount}.</p>"
        f"<p>Дата завершения сбора: {planned_amount}.</p>"
    )

    return subject, message, recipient_list, html_message
