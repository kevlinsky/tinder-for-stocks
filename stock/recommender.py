import numpy as np
from scipy import sparse
import implicit

from app.db import Stock
from app.db import User, UserFavoriteStock


class Recommender:
    async def __make_user_row(self, user_id):
        stocks_count = await Stock.count()
        users_favs = await UserFavoriteStock.get_user_favourites(user_id)

        idx = []
        values = []
        for item in users_favs:
            idx.append(item.stock_id - 1)
            values.append(1.0 / len(users_favs))

        return sparse.coo_matrix(
            (np.array(values).astype(np.float32), ([0] * len(idx), idx)), shape=(1, stocks_count)
        )

    async def fit(self):
        users_favs_count = await UserFavoriteStock.count()
        if self.model is None and users_favs_count > 0:
            users = await User.all()
            rows = []
            for user in users:
                row = await self.__make_user_row(user.id)
                rows.append(row)

            self.sparse_matrix = sparse.vstack(rows)

            self.model = implicit.als.AlternatingLeastSquares(factors=16, regularization=0.0, iterations=8)
            self.model.fit(self.sparse_matrix.T)

    async def recommend(self, user_id, number_of_stocks):
        # row = self.__make_user_row(user_id)
        # recs = self.model.recommend(0, row, N=number_of_stocks,
        #                             filter_already_liked_items=True,
        #                             recalculate_user=True)
        recs = self.model.recommend(0, self.sparse_matrix.getrow(user_id - 1), N=number_of_stocks,
                                    filter_already_liked_items=True,
                                    recalculate_user=False)
        return sorted([int(stock[0] + 1) for stock in recs])

    async def generate_weekly_digest(self):
        if self.model is None:
            await self.fit()

        users = await User.get_weekly_subs()

        digest = []

        for user in users:
            stocks_ids = await self.recommend(user.id, 3)
            stocks = []
            for stock_id in stocks_ids:
                stock = await Stock.get(stock_id)
                stocks.append(stock)

            digest.append({
                'user': user,
                'stocks': stocks
            })

        return digest

    async def generate_monthly_digest(self):
        if self.model is None:
            await self.fit()

        users = await User.get_monthly_subs()

        digest = []

        for user in users:
            stocks_ids = await self.recommend(user.id, 3)
            stocks = []
            for stock_id in stocks_ids:
                stock = await Stock.get(stock_id)
                stocks.append(stock)

            digest.append({
                'user': user,
                'stocks': stocks
            })

        return digest
