
import pandas as pd


def groups_name_inorder(
        df: pd.DataFrame,
        group_col_name: str,
        group_order_col_name: str,
        default_group_name: str,
) -> list[str]:

    rlt = [default_group_name]

    if group_col_name in df and group_order_col_name in df:
        rlt = (
            df.groupby(group_col_name, observed=False)
            .agg({group_order_col_name: 'first'})
            .sort_values(by=group_order_col_name)
            .index
            .to_list()
        )

    elif group_col_name in df:
        rlt = sorted(df[group_col_name].unique())

    return rlt


# sample and/or test code below #################################################################################
if __name__ == '__main__':  # ###################################################################################

    the_df = pd.DataFrame({
        'group': ['group_a', 'group_b', 'group_c'],
        'group_order': [2, 1, 0],
        'random': [0, 10, 20],
    })

    # df_test = df_test.drop(['group_order'], axis=1)
    # df_test = df_test.drop(['group'], axis=1)

    print(groups_name_inorder(the_df, 'group', 'group_order', 'df'))
